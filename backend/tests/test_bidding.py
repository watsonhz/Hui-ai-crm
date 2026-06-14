"""Tests for bidding.py — models + all 6 API endpoints with auth."""

import pytest
from datetime import datetime, timezone, timedelta

from app.models.bidding import Bidding, BID_STATUS_MAP, VALID_BID_TRANSITIONS


# ── Model tests ──────────────────────────────────────────────────────────────


class TestBiddingModel:
    def test_create_minimal(self, db):
        b = Bidding(title="测试投标", bid_status=1)
        db.add(b)
        db.commit()
        db.refresh(b)
        assert b.id is not None
        assert b.bid_status == 1
        assert b.deleted_at is None

    def test_create_with_all_fields(self, db):
        b = Bidding(
            title="华为云投标",
            project_name="华为云DevOps平台",
            bid_amount=500000.00,
            bid_status=2,
            bid_deadline=datetime(2026, 7, 15, tzinfo=timezone.utc),
            submit_deadline=datetime(2026, 7, 10, tzinfo=timezone.utc),
            client_company="华为技术有限公司",
            client_contact="张经理 13800001111",
            description="云平台建设投标",
            notes="重点客户",
            owner_id=1,
        )
        db.add(b)
        db.commit()
        assert b.bid_amount == 500000.00
        assert b.client_company == "华为技术有限公司"

    def test_invalid_status_raises(self):
        b = Bidding(title="test")
        with pytest.raises(ValueError, match="无效的投标状态"):
            b.bid_status = 99

    def test_all_valid_statuses(self):
        b = Bidding(title="test")
        for status in BID_STATUS_MAP:
            b.bid_status = status

    def test_valid_transitions(self):
        b = Bidding(title="test", bid_status=1)
        assert b.can_transition_to(2) is True
        assert b.can_transition_to(8) is True
        assert b.can_transition_to(5) is False

    def test_terminal_status_no_transitions(self):
        b = Bidding(title="test", bid_status=9)
        for status in BID_STATUS_MAP:
            assert b.can_transition_to(status) is False

    def test_paused_can_go_many(self):
        b = Bidding(title="test", bid_status=8)
        assert b.can_transition_to(1) is True
        assert b.can_transition_to(5) is True

    def test_soft_delete_filtered_out(self, db):
        b = Bidding(title="deleted", bid_status=1, deleted_at=datetime.now(timezone.utc))
        db.add(b)
        db.commit()
        result = db.query(Bidding).filter(Bidding.deleted_at.is_(None)).first()
        assert result is None

<<<<<<< HEAD
    def test_default_values(self, db):
        b = Bidding(title="defaults")
        db.add(b)
        db.commit()
        assert b.bid_status == 1
        assert b.created_at is not None
        assert b.updated_at is not None
=======

class TestBiddingAPI:
    def test_create(self, client):
        resp = client.post("/api/v1/bidding/", json={"title": "测试投标", "bid_status": 1, "client_company": "测试公司"})
        assert resp.status_code == 200
        assert resp.json()["data"]["title"] == "测试投标"
>>>>>>> 662f12488696422c660a7b9ff57a0f880cf8e5a8


# ── 401 Unauthorized ─────────────────────────────────────────────────────────

class TestBiddingAPIAuth:
    def test_create_no_auth(self, client):
        r = client.post("/api/v1/bidding/", json={"title": "x"})
        assert r.status_code == 401

    def test_list_no_auth(self, client):
        r = client.get("/api/v1/bidding/")
        assert r.status_code == 401

    def test_get_no_auth(self, client):
        r = client.get("/api/v1/bidding/1")
        assert r.status_code == 401

    def test_update_no_auth(self, client):
        r = client.put("/api/v1/bidding/1", json={"title": "x"})
        assert r.status_code == 401

    def test_calendar_no_auth(self, client):
        r = client.get("/api/v1/bidding/calendar/upcoming")
        assert r.status_code == 401

    def test_malformed_header(self, client):
        r = client.post("/api/v1/bidding/", json={"title": "x"},
                        headers={"Authorization": "NotBearer xyz"})
        assert r.status_code == 401

    def test_invalid_token(self, client):
        r = client.post("/api/v1/bidding/", json={"title": "x"},
                        headers={"Authorization": "Bearer invalid.jwt.token"})
        assert r.status_code == 401


# ── CRUD (authenticated as admin) ────────────────────────────────────────────

class TestBiddingAPICRUD:
    def test_create(self, client, auth_header, admin_user):
        r = client.post("/api/v1/bidding/", json={
            "title": "测试投标", "bid_status": 1, "client_company": "测试公司"
        }, headers={"Authorization": auth_header})
        assert r.status_code == 200
        data = r.json()["data"]
        assert data["title"] == "测试投标"
        assert data["owner_id"] == admin_user.id

    def test_create_validation_error(self, client, auth_header):
        r = client.post("/api/v1/bidding/", json={"title": "x", "bid_status": 99},
                        headers={"Authorization": auth_header})
        assert r.status_code == 422

    def test_get_by_id(self, client, auth_header):
        r = client.post("/api/v1/bidding/", json={"title": "详情测试"},
                        headers={"Authorization": auth_header})
        bid_id = r.json()["data"]["id"]
        r = client.get(f"/api/v1/bidding/{bid_id}",
                       headers={"Authorization": auth_header})
        assert r.status_code == 200
        assert r.json()["data"]["title"] == "详情测试"

    def test_get_not_found(self, client, auth_header):
        r = client.get("/api/v1/bidding/99999",
                       headers={"Authorization": auth_header})
        assert r.status_code == 404

    def test_update_title(self, client, auth_header):
        r = client.post("/api/v1/bidding/", json={"title": "更新前"},
                        headers={"Authorization": auth_header})
        bid_id = r.json()["data"]["id"]
        r = client.put(f"/api/v1/bidding/{bid_id}", json={"title": "更新后"},
                       headers={"Authorization": auth_header})
        assert r.status_code == 200
        assert r.json()["data"]["title"] == "更新后"

    def test_update_status_valid(self, client, auth_header):
        r = client.post("/api/v1/bidding/", json={"title": "状态", "bid_status": 1},
                        headers={"Authorization": auth_header})
        bid_id = r.json()["data"]["id"]
        r = client.put(f"/api/v1/bidding/{bid_id}", json={"bid_status": 2},
                       headers={"Authorization": auth_header})
        assert r.status_code == 200
        assert r.json()["data"]["bid_status"] == 2

    def test_update_status_invalid(self, client, auth_header):
        r = client.post("/api/v1/bidding/", json={"title": "状态", "bid_status": 1},
                        headers={"Authorization": auth_header})
        bid_id = r.json()["data"]["id"]
        r = client.put(f"/api/v1/bidding/{bid_id}", json={"bid_status": 5},
                       headers={"Authorization": auth_header})
        assert r.status_code == 400

    def test_update_not_found(self, client, auth_header):
        r = client.put("/api/v1/bidding/99999", json={"title": "x"},
                       headers={"Authorization": auth_header})
        assert r.status_code == 404


# ── List / Pagination / Filter ───────────────────────────────────────────────

class TestBiddingAPIList:
    def test_list_empty(self, client, auth_header):
        r = client.get("/api/v1/bidding/", headers={"Authorization": auth_header})
        assert r.status_code == 200
        assert r.json()["data"]["items"] == []

    def test_list_pagination(self, client, auth_header):
        for i in range(5):
            client.post("/api/v1/bidding/", json={"title": f"项目{i}"},
                        headers={"Authorization": auth_header})
        r = client.get("/api/v1/bidding/?page=1&page_size=3",
                       headers={"Authorization": auth_header})
        data = r.json()["data"]
        assert data["total"] == 5
        assert len(data["items"]) == 3
        assert data["page"] == 1
        assert data["total_pages"] == 2

    def test_list_page2(self, client, auth_header):
        for i in range(5):
            client.post("/api/v1/bidding/", json={"title": f"项目{i}"},
                        headers={"Authorization": auth_header})
        r = client.get("/api/v1/bidding/?page=2&page_size=3",
                       headers={"Authorization": auth_header})
        assert len(r.json()["data"]["items"]) == 2

    def test_list_filter_by_status(self, client, auth_header):
        client.post("/api/v1/bidding/", json={"title": "意向", "bid_status": 1},
                    headers={"Authorization": auth_header})
        client.post("/api/v1/bidding/", json={"title": "中标", "bid_status": 5},
                    headers={"Authorization": auth_header})
        r = client.get("/api/v1/bidding/?bid_status=5",
                       headers={"Authorization": auth_header})
        assert r.json()["data"]["total"] == 1
        assert r.json()["data"]["items"][0]["bid_status"] == 5

    def test_list_search(self, client, auth_header):
        client.post("/api/v1/bidding/", json={"title": "华为云项目"},
                    headers={"Authorization": auth_header})
        client.post("/api/v1/bidding/", json={"title": "腾讯项目"},
                    headers={"Authorization": auth_header})
        r = client.get("/api/v1/bidding/?search=华为",
                       headers={"Authorization": auth_header})
        assert r.json()["data"]["total"] == 1

    def test_list_search_like_escape(self, client, auth_header):
        """% wildcard is escaped — searching for %% returns literal matches only."""
        client.post("/api/v1/bidding/", json={"title": "普通项目"},
                    headers={"Authorization": auth_header})
        r = client.get("/api/v1/bidding/?search=%%",
                       headers={"Authorization": auth_header})
        assert r.json()["data"]["total"] == 0

    def test_list_sort_asc(self, client, auth_header):
        client.post("/api/v1/bidding/", json={"title": "B"},
                    headers={"Authorization": auth_header})
        client.post("/api/v1/bidding/", json={"title": "A"},
                    headers={"Authorization": auth_header})
        r = client.get("/api/v1/bidding/?sort_order=asc",
                       headers={"Authorization": auth_header})
        items = r.json()["data"]["items"]
        assert items[0]["title"] == "B"
        assert items[1]["title"] == "A"


# ── Authorization (ownership enforcement) ────────────────────────────────────

class TestBiddingAPIAuthz:
    def test_create_owner_is_current_user(self, client, normal_auth_header, normal_user):
        r = client.post("/api/v1/bidding/", json={"title": "我的投标", "bid_status": 1},
                        headers={"Authorization": normal_auth_header})
        assert r.status_code == 200
        assert r.json()["data"]["owner_id"] == normal_user.id

    def test_create_ignores_provided_owner_id(self, client, normal_auth_header, normal_user):
        r = client.post("/api/v1/bidding/",
                        json={"title": "冒充", "bid_status": 1, "owner_id": 1},
                        headers={"Authorization": normal_auth_header})
        assert r.status_code == 200
        assert r.json()["data"]["owner_id"] == normal_user.id

    def test_update_by_owner_succeeds(self, client, normal_auth_header):
        r = client.post("/api/v1/bidding/", json={"title": "我的", "bid_status": 1},
                        headers={"Authorization": normal_auth_header})
        bid_id = r.json()["data"]["id"]
        r = client.put(f"/api/v1/bidding/{bid_id}", json={"title": "改好了"},
                       headers={"Authorization": normal_auth_header})
        assert r.status_code == 200

    def test_update_by_other_user_forbidden(self, client, normal_auth_header, other_auth_header):
        r = client.post("/api/v1/bidding/", json={"title": "A的投标", "bid_status": 1},
                        headers={"Authorization": normal_auth_header})
        bid_id = r.json()["data"]["id"]
        r = client.put(f"/api/v1/bidding/{bid_id}", json={"title": "B篡改"},
                       headers={"Authorization": other_auth_header})
        assert r.status_code == 403

    def test_update_by_admin_succeeds(self, client, normal_auth_header, auth_header):
        r = client.post("/api/v1/bidding/", json={"title": "用户的投标", "bid_status": 1},
                        headers={"Authorization": normal_auth_header})
        bid_id = r.json()["data"]["id"]
        r = client.put(f"/api/v1/bidding/{bid_id}", json={"title": "管理员修改"},
                       headers={"Authorization": auth_header})
        assert r.status_code == 200


# ── Calendar ─────────────────────────────────────────────────────────────────

class TestBiddingAPICalendar:
    def test_calendar_includes_future(self, client, auth_header):
        future = (datetime.now(timezone.utc) + timedelta(days=15)).isoformat()
        client.post("/api/v1/bidding/",
                    json={"title": "即将截止", "bid_deadline": future, "bid_status": 2},
                    headers={"Authorization": auth_header})
        r = client.get("/api/v1/bidding/calendar/upcoming?days=30",
                       headers={"Authorization": auth_header})
        assert len(r.json()["data"]) >= 1

    def test_calendar_excludes_past(self, client, auth_header):
        past = (datetime.now(timezone.utc) - timedelta(days=15)).isoformat()
        client.post("/api/v1/bidding/",
                    json={"title": "已过期", "bid_deadline": past, "bid_status": 3},
                    headers={"Authorization": auth_header})
        r = client.get("/api/v1/bidding/calendar/upcoming?days=30",
                       headers={"Authorization": auth_header})
        titles = [item["title"] for item in r.json()["data"]]
        assert "已过期" not in titles

    def test_calendar_excludes_no_deadline(self, client, auth_header):
        client.post("/api/v1/bidding/", json={"title": "无截止日", "bid_status": 1},
                    headers={"Authorization": auth_header})
        r = client.get("/api/v1/bidding/calendar/upcoming?days=30",
                       headers={"Authorization": auth_header})
        titles = [item["title"] for item in r.json()["data"]]
        assert "无截止日" not in titles
