"""RBAC — deny-by-default, admin override."""

from fastapi import Depends, HTTPException, status
from app.core.security import get_current_user, CurrentUser

ROLE_PERMISSIONS: dict[str, set[str]] = {
    "admin": {
        "bidding:create","bidding:read","bidding:update","bidding:delete",
        "project:create","project:read","project:update","project:delete",
        "customer:create","customer:read","customer:update","customer:delete",
        "organization:create","organization:read","organization:update","organization:delete",
        "workflow:create","workflow:read","workflow:approve","workflow:reject",
        "knowledge:create","knowledge:read","knowledge:delete",
        "report:generate","report:read","audit:read","user:manage",
    },
    "manager": {
        "bidding:create","bidding:read","bidding:update",
        "project:create","project:read","project:update",
        "customer:create","customer:read","customer:update",
        "organization:read","workflow:read","workflow:approve","workflow:reject",
        "knowledge:read","knowledge:create","report:generate","report:read",
    },
    "user": {
        "bidding:create","bidding:read","project:read",
        "customer:create","customer:read","organization:read",
        "workflow:read","knowledge:read","report:generate","report:read",
    },
    "readonly": {
        "bidding:read","project:read","customer:read","organization:read","workflow:read",
    },
}


def require_permission(permission: str):
    def checker(user: CurrentUser = Depends(get_current_user)):
        allowed = ROLE_PERMISSIONS.get(user.role, set())
        if permission not in allowed:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Permission denied: {permission}")
        return True
    return checker


def require_role(*roles: str):
    def checker(user: CurrentUser = Depends(get_current_user)):
        if user.role not in roles:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Requires role: {roles}")
        return True
    return checker
