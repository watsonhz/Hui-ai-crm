from functools import wraps
from fastapi import HTTPException, status
from app.models.user import User

ROLE_PERMISSIONS = {
    "admin": ["*"],
    "manager": ["read", "write", "export"],
    "sales": ["read", "write"],
    "viewer": ["read"],
}

def require_role(*roles: str):
    """限制接口仅允许指定角色访问"""
    def decorator(fn):
        @wraps(fn)
        async def wrapper(*args, **kwargs):
            user: User = kwargs.get("current_user")
            if not user:
                raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="未认证")
            if user.role not in roles:
                raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="权限不足")
            return await fn(*args, **kwargs)
        return wrapper
    return decorator

def has_permission(user: User, action: str) -> bool:
    allowed = ROLE_PERMISSIONS.get(user.role, [])
    return "*" in allowed or action in allowed
