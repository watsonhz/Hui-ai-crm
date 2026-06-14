from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, Request, status
from sqlalchemy.orm import Session
from passlib.hash import bcrypt

from app.core.database import get_db
from app.core.config import settings
from app.core.security import create_access_token, get_current_user, CurrentUser, hash_password, verify_password
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
    username = body.username
    ip = _client_ip(request)

    # Rate limit check (if rate_limit module available)
    try:
        from app.core.rate_limit import login_limiter, brute_force
        if not login_limiter.is_allowed(f"login:{ip}"):
            raise HTTPException(status_code=status.HTTP_429_TOO_MANY_REQUESTS, detail="请求过于频繁")
        if brute_force.is_locked(username):
            raise HTTPException(status_code=status.HTTP_423_LOCKED, detail="账号已临时锁定")
    except ImportError:
        pass

    user = db.query(User).filter(User.username == username).first()

    if not user or not bcrypt.verify(body.password, user.password_hash):
        try:
            from app.core.rate_limit import brute_force
            remaining = brute_force.record_failure(username)
        except ImportError:
            remaining = "?"
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=f"用户名或密码错误（剩余尝试: {remaining}）")

    if not user.is_active:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="账号已禁用")

    try:
        from app.core.rate_limit import brute_force
        brute_force.reset(username)
    except ImportError:
        pass

    token = create_access_token(user.id, user.username, user.role)
    return APIResponse.success(data=TokenResponse(access_token=token, expires_in=settings.JWT_EXPIRE_HOURS))


@router.get("/me", response_model=APIResponse[UserResponse])
def me(user: CurrentUser = Depends(get_current_user), db: Session = Depends(get_db)):
    u = db.query(User).filter(User.id == user.id).first()
    return APIResponse.success(data=UserResponse.model_validate(u))
