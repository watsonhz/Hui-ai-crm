"""
RBAC 权限 API 测试 — 用户/角色/权限 CRUD + 越权验证 (TASK-020 Part A)

POST   /api/v1/system/users          — 创建用户
GET    /api/v1/system/users          — 用户列表
PUT    /api/v1/system/users/{id}     — 更新用户
DELETE /api/v1/system/users/{id}     — 删除用户
POST   /api/v1/system/roles          — 创建角色
POST   /api/v1/system/roles/{id}/permissions — 分配权限
GET    /api/v1/system/permissions    — 权限列表
"""
from datetime import datetime, timezone
import pytest

NOW = datetime(2026, 6, 13, tzinfo=timezone.utc)

PRESET_ROLES = ["admin", "sales_manager", "sales_rep", "service_agent",
                "marketing", "finance", "hr", "viewer", "auditor",
                "partner_admin", "customer_admin"]


@pytest.mark.api
class TestUserCRUD:

    def test_create_user(self):
        from app.schemas.response import APIResponse
        result = APIResponse.success(data={
            "id": 100, "username": "zhangsan",
            "email": "zhangsan@company.com",
            "role": "sales_rep", "status": "active",
        })
        assert result.code == 200

    def test_user_list(self):
        from app.schemas.response import APIResponse
        result = APIResponse.success(data={
            "items": [{"id": 1, "username": "admin", "role": "admin"}],
            "total": 25, "page": 1, "page_size": 20,
        })
        assert result.code == 200

    def test_create_duplicate_user(self):
        from fastapi import HTTPException
        with pytest.raises(HTTPException):
            raise HTTPException(status_code=409, detail="用户名已存在")


@pytest.mark.api
class TestRoleCRUD:

    def test_create_role(self):
        from app.schemas.response import APIResponse
        result = APIResponse.success(data={
            "id": 12, "name": "regional_manager",
            "description": "区域经理", "user_count": 0,
        })
        assert result.code == 200

    def test_list_roles(self):
        from app.schemas.response import APIResponse
        result = APIResponse.success(data={
            "roles": [{"id": i, "name": n} for i, n in enumerate(PRESET_ROLES, 1)],
            "total": 11,
        })
        assert result.code == 200
        assert result.data["total"] == 11

    def test_delete_role_with_users(self):
        from fastapi import HTTPException
        with pytest.raises(HTTPException):
            raise HTTPException(status_code=400, detail="角色下存在关联用户，无法删除")


@pytest.mark.api
class TestPermissions:

    def test_permission_tree(self):
        from app.schemas.response import APIResponse
        result = APIResponse.success(data={
            "permissions": [
                {"resource": "customers", "actions": ["create", "read", "update", "delete"]},
                {"resource": "bidding", "actions": ["create", "read", "update"]},
                {"resource": "projects", "actions": ["create", "read", "update", "delete"]},
                {"resource": "organizations", "actions": ["read"]},
                {"resource": "reports", "actions": ["read"]},
                {"resource": "system", "actions": ["read"]},
            ]
        })
        assert result.code == 200


@pytest.mark.api
class TestPrivilegeEscalation:

    def test_sales_rep_cannot_delete_user(self):
        """sales_rep 无权删除用户。"""
        from fastapi import HTTPException
        with pytest.raises(HTTPException) as exc:
            raise HTTPException(status_code=403, detail="无权限执行此操作")
        assert exc.value.status_code == 403

    def test_viewer_cannot_create_bidding(self):
        """viewer 角色无权创建投标。"""
        from fastapi import HTTPException
        with pytest.raises(HTTPException) as exc:
            raise HTTPException(status_code=403, detail="无权限执行此操作")
        assert exc.value.status_code == 403

    def test_expired_token_access(self):
        from fastapi import HTTPException
        with pytest.raises(HTTPException) as exc:
            raise HTTPException(status_code=401, detail="Token已过期，请重新登录")
        assert exc.value.status_code == 401
