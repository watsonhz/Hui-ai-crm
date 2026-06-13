"""Tests for customers.py — models + all 5 API endpoints with auth."""

import pytest
from datetime import datetime, timezone

from app.models.customer import Customer, VALID_LEVELS, VALID_STATUSES


# ── Model tests ──────────────────────────────────────────────────────────────

class TestCustomerModel:
    def test_create(self, db):
        c = Customer(name="张三", company="华为", phone="13800001111")
        db.add(c)
        db.commit()
        db.refresh(c)
        assert c.id is not None
        assert c.level == "C"
        assert c.status == "潜在"

    def test_invalid_level(self):
        c = Customer(name="test")
        with pytest.raises(ValueError, match="无效的客户等级"):
            c.level = "X"

    def test_invalid_status(self):
        c = Customer(name="test")
        with pytest.raises(ValueError, match="无效的客户状态"):
            c.status = "无效"

    def test_all_valid_levels(self):
        c = Customer(name="test")
        for lvl in VALID_LEVELS:
            c.level = lvl

    def test_all_valid_statuses(self):
        c = Customer(name="test")
        for st in VALID_STATUSES:
            c.status = st

    def test_soft_delete(self, db):
        c = Customer(name="deleted", deleted_at=datetime.now(timezone.utc))
        db.add(c)
        db.commit()
        result = db.query(Customer).filter(Customer.deleted_at.is_(None)).first()
        assert result is None


# ── 401 Unauthorized ─────────────────────────────────────────────────────────

class TestCustomersAPIAuth:
    def test_create_no_auth(self, client):
        r = client.post("/api/v1/customers/", json={"name": "x"})
        assert r.status_code == 401

    def test_list_no_auth(self, client):
        r = client.get("/api/v1/customers/")
        assert r.status_code == 401

    def test_get_no_auth(self, client):
        r = client.get("/api/v1/customers/1")
        assert r.status_code == 401

    def test_update_no_auth(self, client):
        r = client.put("/api/v1/customers/1", json={"name": "x"})
        assert r.status_code == 401

    def test_delete_no_auth(self, client):
        r = client.delete("/api/v1/customers/1")
        assert r.status_code == 401


# ── CRUD ─────────────────────────────────────────────────────────────────────

class TestCustomersAPICRUD:
    def test_create(self, client, auth_header, admin_user):
        r = client.post("/api/v1/customers/", json={
            "name": "张三", "company": "华为技术", "phone": "13800001111",
            "email": "zhangsan@huawei.com", "level": "A", "status": "意向"
        }, headers={"Authorization": auth_header})
        assert r.status_code == 200
        data = r.json()["data"]
        assert data["name"] == "张三"
        assert data["owner_id"] == admin_user.id
        assert data["level"] == "A"

    def test_create_validation_invalid_email(self, client, auth_header):
        r = client.post("/api/v1/customers/", json={"name": "x", "email": "not-email"},
                        headers={"Authorization": auth_header})
        assert r.status_code == 422

    def test_create_validation_invalid_level(self, client, auth_header):
        r = client.post("/api/v1/customers/", json={"name": "x", "level": "X"},
                        headers={"Authorization": auth_header})
        assert r.status_code == 422

    def test_get_by_id(self, client, auth_header):
        r = client.post("/api/v1/customers/", json={"name": "李四"},
                        headers={"Authorization": auth_header})
        cid = r.json()["data"]["id"]
        r = client.get(f"/api/v1/customers/{cid}", headers={"Authorization": auth_header})
        assert r.json()["data"]["name"] == "李四"

    def test_get_not_found(self, client, auth_header):
        r = client.get("/api/v1/customers/99999", headers={"Authorization": auth_header})
        assert r.status_code == 404

    def test_update(self, client, auth_header):
        r = client.post("/api/v1/customers/", json={"name": "旧名"},
                        headers={"Authorization": auth_header})
        cid = r.json()["data"]["id"]
        r = client.put(f"/api/v1/customers/{cid}", json={"name": "新名"},
                       headers={"Authorization": auth_header})
        assert r.json()["data"]["name"] == "新名"

    def test_delete(self, client, auth_header):
        r = client.post("/api/v1/customers/", json={"name": "待删"},
                        headers={"Authorization": auth_header})
        cid = r.json()["data"]["id"]
        r = client.delete(f"/api/v1/customers/{cid}",
                          headers={"Authorization": auth_header})
        assert r.status_code == 200
        # verify soft deleted
        r = client.get(f"/api/v1/customers/{cid}", headers={"Authorization": auth_header})
        assert r.status_code == 404

    def test_delete_not_found(self, client, auth_header):
        r = client.delete("/api/v1/customers/99999", headers={"Authorization": auth_header})
        assert r.status_code == 404


# ── List / Filter / Pagination ───────────────────────────────────────────────

class TestCustomersAPIList:
    def test_list_empty(self, client, auth_header):
        r = client.get("/api/v1/customers/", headers={"Authorization": auth_header})
        assert r.json()["data"]["items"] == []

    def test_list_pagination(self, client, auth_header):
        for i in range(5):
            client.post("/api/v1/customers/", json={"name": f"客户{i}"},
                        headers={"Authorization": auth_header})
        r = client.get("/api/v1/customers/?page=1&page_size=3",
                       headers={"Authorization": auth_header})
        data = r.json()["data"]
        assert data["total"] == 5
        assert len(data["items"]) == 3

    def test_filter_by_status(self, client, auth_header):
        client.post("/api/v1/customers/", json={"name": "a", "status": "潜在"},
                    headers={"Authorization": auth_header})
        client.post("/api/v1/customers/", json={"name": "b", "status": "成交"},
                    headers={"Authorization": auth_header})
        r = client.get("/api/v1/customers/?status=成交",
                       headers={"Authorization": auth_header})
        assert r.json()["data"]["total"] == 1

    def test_filter_by_level(self, client, auth_header):
        client.post("/api/v1/customers/", json={"name": "a", "level": "A"},
                    headers={"Authorization": auth_header})
        client.post("/api/v1/customers/", json={"name": "b", "level": "B"},
                    headers={"Authorization": auth_header})
        r = client.get("/api/v1/customers/?level=A",
                       headers={"Authorization": auth_header})
        assert r.json()["data"]["total"] == 1

    def test_search_by_name(self, client, auth_header):
        client.post("/api/v1/customers/", json={"name": "华为云科技"},
                    headers={"Authorization": auth_header})
        client.post("/api/v1/customers/", json={"name": "腾讯云计算"},
                    headers={"Authorization": auth_header})
        r = client.get("/api/v1/customers/?name=华为",
                       headers={"Authorization": auth_header})
        assert r.json()["data"]["total"] == 1

    def test_search_by_company(self, client, auth_header):
        client.post("/api/v1/customers/", json={"name": "a", "company": "中科曙光"},
                    headers={"Authorization": auth_header})
        client.post("/api/v1/customers/", json={"name": "b", "company": "浪潮电子"},
                    headers={"Authorization": auth_header})
        r = client.get("/api/v1/customers/?company=曙光",
                       headers={"Authorization": auth_header})
        assert r.json()["data"]["total"] == 1

    def test_sort_asc(self, client, auth_header):
        client.post("/api/v1/customers/", json={"name": "B"},
                    headers={"Authorization": auth_header})
        client.post("/api/v1/customers/", json={"name": "A"},
                    headers={"Authorization": auth_header})
        r = client.get("/api/v1/customers/?sort_order=asc",
                       headers={"Authorization": auth_header})
        items = r.json()["data"]["items"]
        assert items[0]["name"] == "B"


# ── Authorization ────────────────────────────────────────────────────────────

class TestCustomersAPIAuthz:
    def test_create_owner_is_current_user(self, client, normal_auth_header, normal_user):
        r = client.post("/api/v1/customers/", json={"name": "我的客户"},
                        headers={"Authorization": normal_auth_header})
        assert r.json()["data"]["owner_id"] == normal_user.id

    def test_update_by_other_user_forbidden(self, client, normal_auth_header, other_auth_header):
        r = client.post("/api/v1/customers/", json={"name": "A的客户"},
                        headers={"Authorization": normal_auth_header})
        cid = r.json()["data"]["id"]
        r = client.put(f"/api/v1/customers/{cid}", json={"name": "B篡改"},
                       headers={"Authorization": other_auth_header})
        assert r.status_code == 403

    def test_delete_by_other_user_forbidden(self, client, normal_auth_header, other_auth_header):
        r = client.post("/api/v1/customers/", json={"name": "A的客户"},
                        headers={"Authorization": normal_auth_header})
        cid = r.json()["data"]["id"]
        r = client.delete(f"/api/v1/customers/{cid}",
                          headers={"Authorization": other_auth_header})
        assert r.status_code == 403

    def test_update_by_admin_succeeds(self, client, normal_auth_header, auth_header):
        r = client.post("/api/v1/customers/", json={"name": "用户的客户"},
                        headers={"Authorization": normal_auth_header})
        cid = r.json()["data"]["id"]
        r = client.put(f"/api/v1/customers/{cid}", json={"name": "管理员修改"},
                       headers={"Authorization": auth_header})
        assert r.status_code == 200
