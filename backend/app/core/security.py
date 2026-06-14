"""JWT Authentication & Authorization module."""

from datetime import datetime, timedelta, timezone
from dataclasses import dataclass

from fastapi import Depends, HTTPException, Header, status
from jose import JWTError, jwt
<<<<<<< HEAD
=======
from passlib.context import CryptContext
>>>>>>> 662f12488696422c660a7b9ff57a0f880cf8e5a8
from sqlalchemy.orm import Session

from app.core.config import settings
from app.core.database import get_db
from app.models.user import User

<<<<<<< HEAD
=======
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain: str, hashed: str) -> bool:
    return pwd_context.verify(plain, hashed)

>>>>>>> 662f12488696422c660a7b9ff57a0f880cf8e5a8

@dataclass
class CurrentUser:
    """Lightweight authenticated user context injected into endpoints."""
    id: int
    username: str
    role: str


def create_access_token(user_id: int, username: str, role: str = "user") -> str:
    """Generate a signed JWT access token."""
    payload = {
        "sub": str(user_id),
        "username": username,
        "role": role,
        "iat": datetime.now(timezone.utc),
        "exp": datetime.now(timezone.utc) + timedelta(hours=settings.JWT_EXPIRE_HOURS),
    }
    return jwt.encode(payload, settings.SECRET_KEY, algorithm=settings.JWT_ALGORITHM)


def decode_token(token: str) -> dict:
    """Decode and verify a JWT token. Raises HTTPException on failure."""
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.JWT_ALGORITHM])
        if payload.get("sub") is None:
<<<<<<< HEAD
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token无效: 缺少用户标识",
            )
        return payload
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token无效或已过期",
        )
=======
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token无效")
        return payload
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token无效或已过期")
>>>>>>> 662f12488696422c660a7b9ff57a0f880cf8e5a8


def get_current_user(
    authorization: str = Header(None, description="Bearer <JWT Token>"),
    db: Session = Depends(get_db),
) -> CurrentUser:
    """FastAPI dependency: validate JWT and return the authenticated user."""
    if not authorization:
<<<<<<< HEAD
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="缺少认证令牌",
        )
    if not authorization.startswith("Bearer "):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="认证头格式错误，应为 'Bearer <token>'",
        )
    token = authorization[7:]
    payload = decode_token(token)
    user_id = int(payload["sub"])

    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="用户不存在或已禁用",
        )
    return CurrentUser(id=user.id, username=user.username, role=user.role)
=======
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="缺少认证令牌")
    if not authorization.startswith("Bearer "):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="认证头格式错误")
    token = authorization[7:]
    payload = decode_token(token)
    user_id = int(payload["sub"])
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="用户不存在或已禁用")
    return CurrentUser(id=user.id, username=user.username, role=user.role)


def require_auth(current_user: CurrentUser = Depends(get_current_user)):
    """Require authentication or raise 401."""
    return current_user
>>>>>>> 662f12488696422c660a7b9ff57a0f880cf8e5a8
