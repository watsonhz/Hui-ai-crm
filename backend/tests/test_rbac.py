"""Tests for RBAC permissions."""
from app.core.rbac import ROLE_PERMISSIONS

class TestRBAC:
    def test_admin_has_all(self): assert len(ROLE_PERMISSIONS["admin"]) > 20
    def test_readonly_cannot_write(self): assert "customer:create" not in ROLE_PERMISSIONS["readonly"]
    def test_deny_by_default(self): assert ROLE_PERMISSIONS.get("hacker", set()) == set()
    def test_user_cannot_manage(self): assert "user:manage" not in ROLE_PERMISSIONS["user"]
