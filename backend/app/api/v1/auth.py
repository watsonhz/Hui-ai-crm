"""Authentication endpoints: login, token refresh."""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from passlib.hash import bcrypt

from app.core.database import get_db
from app.core.config import settings
from app.core.security import create_access_token, get_current_user, CurrentUser
from app.models.user import User
from app.schemas.user import UserLogin, TokenResponse, UserResponse
from app.schemas.response import APIResponse

router = APIRouter()


@router.post("/login", response_model=APIResponse[TokenResponse])
def login(body: UserLogin, db: Session = Depends(get_db)):
    """Authenticate with username + password, return JWT token."""
    user = db.query(User).filter(User.username == body.username).first()
    if not user or not bcrypt.verify(body.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="用户名或密码错误",
        )
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="账号已被禁用",
        )
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
