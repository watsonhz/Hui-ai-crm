"""Tests for organizations.py — models + all 5 API endpoints with auth."""

import pytest
from datetime import datetime, timezone

from app.models.organization import Organization, ORG_TYPES


# ── Model tests ──────────────────────────────────────────────────────────────

class TestOrganizationModel:
    def test_create(self, db):
        org = Organization(name="技术部", org_type="dept")
        db.add(org)
        db.commit()
        db.refresh(org)
        assert org.id is not None
        assert org.deleted_at is None

    def test_parent_child(self, db):
        parent = Organization(name="总公司", org_type="company")
        db.add(parent)
        db.commit()
        child = Organization(name="研发部", org_type="dept", parent_id=parent.id)
        db.add(child)
        db.commit()
        assert child.parent_id == parent.id

    def test_invalid_type_raises(self):
        org = Organization(name="test")
        with pytest.raises(ValueError, match="无效的组织类型"):
            org.org_type = "invalid"

    def test_all_valid_types(self):
        org = Organization(name="test")
        for t in ORG_TYPES:
            org.org_type = t

    def test_default_values(self, db):
        org = Organization(name="defaults")
        db.add(org)
        db.commit()
        assert org.org_type == "dept"
        assert org.sort_order == 0

    def test_soft_delete_filtered_out(self, db):
        org = Organization(name="deleted", deleted_at=datetime.now(timezone.utc))
        db.add(org)
        db.commit()
        result = db.query(Organization).filter(Organization.deleted_at.is_(None)).first()
        assert result is None


# ── 401 Unauthorized ─────────────────────────────────────────────────────────

class TestOrganizationsAPIAuth:
    def test_create_no_auth(self, client):
        r = client.post("/api/v1/organizations/", json={"name": "x"})
        assert r.status_code == 401

    def test_tree_no_auth(self, client):
        r = client.get("/api/v1/organizations/tree")
        assert r.status_code == 401

    def test_update_no_auth(self, client):
        r = client.put("/api/v1/organizations/1", json={"name": "x"})
        assert r.status_code == 401

    def test_delete_no_auth(self, client):
        r = client.delete("/api/v1/organizations/1")
        assert r.status_code == 401


# ── CRUD (authenticated as admin) ────────────────────────────────────────────

class TestOrganizationsAPICRUD:
    def test_create_company(self, client, auth_header):
        r = client.post("/api/v1/organizations/",
                        json={"name": "总公司", "org_type": "company"},
                        headers={"Authorization": auth_header})
        assert r.status_code == 200
        assert r.json()["data"]["org_type"] == "company"

    def test_create_with_parent(self, client, auth_header):
        r = client.post("/api/v1/organizations/",
                        json={"name": "总公司", "org_type": "company"},
                        headers={"Authorization": auth_header})
        pid = r.json()["data"]["id"]
        r = client.post("/api/v1/organizations/",
                        json={"name": "研发部", "org_type": "dept", "parent_id": pid},
                        headers={"Authorization": auth_header})
        assert r.status_code == 200
        assert r.json()["data"]["parent_id"] == pid

    def test_create_invalid_org_type(self, client, auth_header):
        r = client.post("/api/v1/organizations/",
                        json={"name": "test", "org_type": "invalid"},
                        headers={"Authorization": auth_header})
        assert r.status_code == 422

    def test_create_nonexistent_parent(self, client, auth_header):
        r = client.post("/api/v1/organizations/",
                        json={"name": "孤立部门", "parent_id": 99999},
                        headers={"Authorization": auth_header})
        assert r.status_code == 400

    def test_update(self, client, auth_header):
        r = client.post("/api/v1/organizations/",
                        json={"name": "旧名称"},
                        headers={"Authorization": auth_header})
        oid = r.json()["data"]["id"]
        r = client.put(f"/api/v1/organizations/{oid}",
                       json={"name": "新名称"},
                       headers={"Authorization": auth_header})
        assert r.json()["data"]["name"] == "新名称"

    def test_update_not_found(self, client, auth_header):
        r = client.put("/api/v1/organizations/99999",
                       json={"name": "x"},
                       headers={"Authorization": auth_header})
        assert r.status_code == 404

    def test_update_self_parent(self, client, auth_header):
        """Cannot set an org's parent to itself."""
        r = client.post("/api/v1/organizations/",
                        json={"name": "自引用"},
                        headers={"Authorization": auth_header})
        oid = r.json()["data"]["id"]
        r = client.put(f"/api/v1/organizations/{oid}",
                       json={"parent_id": oid},
                       headers={"Authorization": auth_header})
        assert r.status_code == 400

    def test_update_circular_ref(self, client, auth_header):
        """A→B→C, then C→A should be blocked."""
        r = client.post("/api/v1/organizations/",
                        json={"name": "A"},
                        headers={"Authorization": auth_header})
        aid = r.json()["data"]["id"]
        r = client.post("/api/v1/organizations/",
                        json={"name": "B", "parent_id": aid},
                        headers={"Authorization": auth_header})
        bid = r.json()["data"]["id"]
        r = client.post("/api/v1/organizations/",
                        json={"name": "C", "parent_id": bid},
                        headers={"Authorization": auth_header})
        cid = r.json()["data"]["id"]
        # Try to make A a child of C → cycle A→B→C→A
        r = client.put(f"/api/v1/organizations/{aid}",
                       json={"parent_id": cid},
                       headers={"Authorization": auth_header})
        assert r.status_code == 400

    def test_delete(self, client, auth_header):
        r = client.post("/api/v1/organizations/",
                        json={"name": "待删除"},
                        headers={"Authorization": auth_header})
        oid = r.json()["data"]["id"]
        r = client.delete(f"/api/v1/organizations/{oid}",
                          headers={"Authorization": auth_header})
        assert r.status_code == 200
        assert r.json()["message"] == "删除成功"

    def test_delete_rejects_parent_with_children(self, client, auth_header):
        r = client.post("/api/v1/organizations/",
                        json={"name": "父节点"},
                        headers={"Authorization": auth_header})
        pid = r.json()["data"]["id"]
        client.post("/api/v1/organizations/",
                    json={"name": "子节点", "parent_id": pid},
                    headers={"Authorization": auth_header})
        r = client.delete(f"/api/v1/organizations/{pid}",
                          headers={"Authorization": auth_header})
        assert r.status_code == 400

    def test_delete_not_found(self, client, auth_header):
        r = client.delete("/api/v1/organizations/99999",
                          headers={"Authorization": auth_header})
        assert r.status_code == 404


# ── Tree ─────────────────────────────────────────────────────────────────────

class TestOrganizationsAPITree:
    def test_tree_empty(self, client, auth_header):
        r = client.get("/api/v1/organizations/tree",
                       headers={"Authorization": auth_header})
        assert r.status_code == 200
        assert r.json()["data"] == []

    def test_tree_single_root(self, client, auth_header):
        client.post("/api/v1/organizations/",
                    json={"name": "公司", "org_type": "company"},
                    headers={"Authorization": auth_header})
        data = client.get("/api/v1/organizations/tree",
                          headers={"Authorization": auth_header}).json()["data"]
        assert len(data) == 1
        assert data[0]["children"] == []

    def test_tree_nested(self, client, auth_header):
        r = client.post("/api/v1/organizations/",
                        json={"name": "总公司", "org_type": "company"},
                        headers={"Authorization": auth_header})
        pid = r.json()["data"]["id"]
        client.post("/api/v1/organizations/",
                    json={"name": "研发", "org_type": "dept", "parent_id": pid},
                    headers={"Authorization": auth_header})
        client.post("/api/v1/organizations/",
                    json={"name": "销售", "org_type": "dept", "parent_id": pid},
                    headers={"Authorization": auth_header})
        data = client.get("/api/v1/organizations/tree",
                          headers={"Authorization": auth_header}).json()["data"]
        assert len(data) == 1
        assert len(data[0]["children"]) == 2

    def test_tree_deep_nesting(self, client, auth_header):
        """A(root)→B→C: only A is root, B under A.children, C under B.children."""
        r = client.post("/api/v1/organizations/",
                        json={"name": "A", "org_type": "company"},
                        headers={"Authorization": auth_header})
        aid = r.json()["data"]["id"]
        r = client.post("/api/v1/organizations/",
                        json={"name": "B", "parent_id": aid},
                        headers={"Authorization": auth_header})
        bid = r.json()["data"]["id"]
        client.post("/api/v1/organizations/",
                    json={"name": "C", "parent_id": bid},
                    headers={"Authorization": auth_header})
        data = client.get("/api/v1/organizations/tree",
                          headers={"Authorization": auth_header}).json()["data"]
        assert len(data) == 1
        assert data[0]["name"] == "A"
        assert len(data[0]["children"]) == 1
        assert data[0]["children"][0]["name"] == "B"
        assert len(data[0]["children"][0]["children"]) == 1
        assert data[0]["children"][0]["children"][0]["name"] == "C"
