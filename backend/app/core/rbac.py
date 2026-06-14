<<<<<<< HEAD
"""RBAC Role-Based Access Control — deny-by-default, admin override.

Roles: admin, manager, user, readonly
Permissions checked per-endpoint via dependency injection.
"""

from dataclasses import dataclass
from fastapi import Depends, HTTPException, status
from app.core.security import get_current_user, CurrentUser


# Permission definitions
ROLE_PERMISSIONS: dict[str, set[str]] = {
    "admin": {
        "bidding:create", "bidding:read", "bidding:update", "bidding:delete",
        "project:create", "project:read", "project:update", "project:delete",
        "customer:create", "customer:read", "customer:update", "customer:delete",
        "organization:create", "organization:read", "organization:update", "organization:delete",
        "workflow:create", "workflow:read", "workflow:approve", "workflow:reject",
        "knowledge:create", "knowledge:read", "knowledge:delete",
        "report:generate", "report:read",
        "audit:read", "user:manage",
    },
    "manager": {
        "bidding:create", "bidding:read", "bidding:update",
        "project:create", "project:read", "project:update",
        "customer:create", "customer:read", "customer:update",
        "organization:read",
        "workflow:read", "workflow:approve", "workflow:reject",
        "knowledge:read", "knowledge:create",
        "report:generate", "report:read",
    },
    "user": {
        "bidding:create", "bidding:read",
        "project:read",
        "customer:create", "customer:read",
        "organization:read",
        "workflow:read",
        "knowledge:read",
        "report:generate", "report:read",
    },
    "readonly": {
        "bidding:read",
        "project:read",
        "customer:read",
        "organization:read",
        "workflow:read",
=======
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
>>>>>>> 662f12488696422c660a7b9ff57a0f880cf8e5a8
    },
}


def require_permission(permission: str):
<<<<<<< HEAD
    """FastAPI dependency: enforce specific permission.

    Usage:
        @router.delete("/{id}")
        def delete(id: int, user=Depends(get_current_user), _=Depends(require_permission("customer:delete"))):
            ...
    """
    def checker(user: CurrentUser = Depends(get_current_user)):
        allowed = ROLE_PERMISSIONS.get(user.role, set())
        if permission not in allowed:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"权限不足: 需要 {permission}",
            )
=======
    def checker(user: CurrentUser = Depends(get_current_user)):
        allowed = ROLE_PERMISSIONS.get(user.role, set())
        if permission not in allowed:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Permission denied: {permission}")
>>>>>>> 662f12488696422c660a7b9ff57a0f880cf8e5a8
        return True
    return checker


def require_role(*roles: str):
<<<<<<< HEAD
    """FastAPI dependency: enforce minimum role level.

    Usage:
        @router.get("/admin/users")
        def list_users(user=Depends(get_current_user), _=Depends(require_role("admin"))):
            ...
    """
    def checker(user: CurrentUser = Depends(get_current_user)):
        if user.role not in roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"需要角色: {roles}",
            )
=======
    def checker(user: CurrentUser = Depends(get_current_user)):
        if user.role not in roles:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Requires role: {roles}")
>>>>>>> 662f12488696422c660a7b9ff57a0f880cf8e5a8
        return True
    return checker
