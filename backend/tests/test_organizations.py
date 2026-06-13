from datetime import datetime, timezone
from app.models.organization import Organization

class TestOrganizationModel:
    def test_create(self, db):
        org = Organization(name="技术部", org_type="dept")
        db.add(org)
        db.commit()
        assert org.id is not None

    def test_parent_child(self, db):
        parent = Organization(name="总公司", org_type="company")
        db.add(parent)
        db.commit()
        child = Organization(name="研发部", org_type="dept", parent_id=parent.id)
        db.add(child)
        db.commit()
        assert child.parent_id == parent.id

    def test_invalid_type(self):
        org = Organization(name="test")
        try:
            org.org_type = "invalid"
            assert False
        except ValueError:
            pass

    def test_soft_delete(self, db):
        org = Organization(name="待删除", deleted_at=datetime.now(timezone.utc))
        db.add(org)
        db.commit()
        result = db.query(Organization).filter(Organization.deleted_at.is_(None)).first()
        assert result is None

class TestOrganizationsAPI:
    def test_create_company(self, client):
        resp = client.post("/api/v1/organizations/", json={"name": "总公司", "org_type": "company"})
        assert resp.json()["data"]["org_type"] == "company"

    def test_create_with_parent(self, client):
        r = client.post("/api/v1/organizations/", json={"name": "总公司", "org_type": "company"})
        pid = r.json()["data"]["id"]
        resp = client.post("/api/v1/organizations/", json={"name": "研发部", "org_type": "dept", "parent_id": pid})
        assert resp.json()["data"]["parent_id"] == pid

    def test_create_invalid_org_type(self, client):
        resp = client.post("/api/v1/organizations/", json={"name": "test", "org_type": "invalid"})
        assert resp.status_code == 422

    def test_create_nonexistent_parent(self, client):
        resp = client.post("/api/v1/organizations/", json={"name": "孤立部门", "parent_id": 99999})
        assert resp.status_code == 400

    def test_tree(self, client):
        r = client.post("/api/v1/organizations/", json={"name": "总公司", "org_type": "company"})
        pid = r.json()["data"]["id"]
        client.post("/api/v1/organizations/", json={"name": "研发", "org_type": "dept", "parent_id": pid})
        client.post("/api/v1/organizations/", json={"name": "销售", "org_type": "dept", "parent_id": pid})
        data = client.get("/api/v1/organizations/tree").json()["data"]
        assert len(data) == 1
        assert len(data[0]["children"]) == 2

    def test_update(self, client):
        r = client.post("/api/v1/organizations/", json={"name": "旧名称"})
        oid = r.json()["data"]["id"]
        resp = client.put(f"/api/v1/organizations/{oid}", json={"name": "新名称"})
        assert resp.json()["data"]["name"] == "新名称"

    def test_delete(self, client):
        r = client.post("/api/v1/organizations/", json={"name": "待删除"})
        oid = r.json()["data"]["id"]
        resp = client.delete(f"/api/v1/organizations/{oid}")
        assert resp.json()["message"] == "删除成功"

    def test_delete_rejects_parent_with_children(self, client):
        r = client.post("/api/v1/organizations/", json={"name": "有子节点"})
        pid = r.json()["data"]["id"]
        client.post("/api/v1/organizations/", json={"name": "子节点", "parent_id": pid})
        resp = client.delete(f"/api/v1/organizations/{pid}")
        assert resp.status_code == 400
