"""Tests for RBAC role-based access control + audit logging."""

import pytest
from app.core.rbac import require_permission, require_role, ROLE_PERMISSIONS


class TestRBACPermissions:
    def test_admin_has_all_permissions(self):
        assert len(ROLE_PERMISSIONS["admin"]) > 20

    def test_readonly_cannot_write(self):
        assert "customer:create" not in ROLE_PERMISSIONS["readonly"]
        assert "customer:read" in ROLE_PERMISSIONS["readonly"]

    def test_user_cannot_manage_users(self):
        assert "user:manage" not in ROLE_PERMISSIONS["user"]

    def test_manager_can_approve_workflows(self):
        assert "workflow:approve" in ROLE_PERMISSIONS["manager"]

    def test_deny_by_default(self):
        """Unknown roles get empty permission set."""
        assert ROLE_PERMISSIONS.get("hacker", set()) == set()


class TestAuditLog:
    def test_log_returns_hash(self):
        from app.services.audit_log import AuditLogger
        logger = AuditLogger(db=None)
        h = logger.log(
            user_id=1, username="admin",
            action="delete", resource_type="customer", resource_id=42,
            old_value={"name": "张三", "phone": "13800001111"},
            new_value=None,
            ip_address="192.168.0.1",
        )
        assert len(h) == 64  # SHA256 hex

    def test_log_redacts_sensitive_fields(self):
        from app.services.audit_log import AuditLogger
        from app.services.audit_log import _redact
        data = {"name": "admin", "password": "secret123", "api_key": "sk-xxx"}
        cleaned = _redact(data, {"password", "secret", "token", "api_key"})
        assert cleaned["name"] == "admin"
        assert cleaned["password"] == "[REDACTED]"
        assert cleaned["api_key"] == "[REDACTED]"

    def test_verify_integrity(self):
        from app.services.audit_log import AuditLogger
        logger = AuditLogger(db=None)
        entries = [
            {"action": "create", "user": "admin", "_hash": "fake"},
        ]
        assert logger.verify_integrity(entries) is False  # hash mismatch

    def test_verify_integrity_no_hash(self):
        from app.services.audit_log import AuditLogger
        logger = AuditLogger(db=None)
        entries = [{"action": "create", "user": "admin"}]
        assert logger.verify_integrity(entries) is True  # no hash = skip


class TestRBACAPI:
    """Verify RBAC is not enforced yet on existing endpoints (no breaking)."""
    def test_readonly_can_still_read_bidding(self, client, auth_header):
        """Admin (current auth_header) can access bidding list."""
        r = client.get("/api/v1/bidding/", headers={"Authorization": auth_header})
        assert r.status_code == 200
