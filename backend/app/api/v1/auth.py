from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, Request, status
from sqlalchemy.orm import Session
from passlib.hash import bcrypt

from app.core.database import get_db
from app.core.config import settings
from app.core.security import create_access_token, get_current_user, CurrentUser
from app.core.rate_limit import login_limiter, brute_force
from app.models.user import User
from app.schemas.user import UserLogin, TokenResponse, UserResponse
from app.schemas.response import APIResponse

router = APIRouter()


def _client_ip(request: Request) -> str:
    forwarded = request.headers.get("X-Forwarded-For")
    if forwarded:
        return forwarded.split(",")[0].strip()
    return request.client.host if request.client else "unknown"


@router.post("/login", response_model=APIResponse[TokenResponse])
def login(body: UserLogin, request: Request, db: Session = Depends(get_db)):
    """Authenticate with username + password. Rate-limited, brute-force protected."""
    username = body.username
    ip = _client_ip(request)

    # Rate limit: 5 login attempts per minute per IP
    if not login_limiter.is_allowed(f"login:{ip}"):
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail="请求过于频繁，请稍后再试",
        )

    # Brute-force check: account locked?
    if brute_force.is_locked(username):
        raise HTTPException(
            status_code=status.HTTP_423_LOCKED,
            detail=f"账号已被临时锁定（连续{brute_force.MAX_FAILURES}次失败），请{brute_force.LOCK_MINUTES}分钟后再试",
        )

    user = db.query(User).filter(User.username == username).first()

    if not user or not bcrypt.verify(body.password, user.password_hash):
        remaining = brute_force.record_failure(username)
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"用户名或密码错误（剩余尝试次数: {remaining}）",
        )

    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="账号已被禁用",
        )

    # Success: reset failure counter
    brute_force.reset(username)

    token = create_access_token(user.id, user.username, user.role)
    return APIResponse.success(data=TokenResponse(
        access_token=token,
        expires_in=settings.JWT_EXPIRE_HOURS,
    ))


@router.get("/me", response_model=APIResponse[UserResponse])
def me(user: CurrentUser = Depends(get_current_user), db: Session = Depends(get_db)):
    """Return the current authenticated user's profile."""
    u = db.query(User).filter(User.id == user.id).first()
    return APIResponse.success(data=UserResponse.model_validate(u))
