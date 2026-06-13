from datetime import datetime, timezone, timedelta
from app.models.bidding import Bidding

class TestBiddingModel:
    def test_create(self, db):
        b = Bidding(title="测试投标", bid_status=1)
        db.add(b)
        db.commit()
        assert b.id is not None

    def test_invalid_status(self):
        b = Bidding(title="test")
        try:
            b.bid_status = 99
            assert False
        except ValueError:
            pass

    def test_valid_transition(self, db):
        b = Bidding(title="test", bid_status=1)
        db.add(b)
        db.commit()
        assert b.can_transition_to(2) is True
        assert b.can_transition_to(5) is False

    def test_soft_delete(self, db):
        b = Bidding(title="test", bid_status=1, deleted_at=datetime.now(timezone.utc))
        db.add(b)
        db.commit()
        result = db.query(Bidding).filter(Bidding.deleted_at.is_(None)).first()
        assert result is None

class TestBiddingAPI:
    def test_create(self, client):
        resp = client.post("/api/v1/bidding/", json={"title": "测试投标", "bid_status": 1, "client_company": "测试公司"})
        assert resp.status_code == 200
        assert resp.json()["data"]["title"] == "测试投标"

    def test_create_invalid_status(self, client):
        resp = client.post("/api/v1/bidding/", json={"title": "test", "bid_status": 99})
        assert resp.status_code == 422

    def test_list_empty(self, client):
        resp = client.get("/api/v1/bidding/")
        assert resp.json()["data"]["items"] == []

    def test_list_with_pagination(self, client):
        for i in range(5):
            client.post("/api/v1/bidding/", json={"title": f"项目{i}"})
        resp = client.get("/api/v1/bidding/?page=1&page_size=3")
        data = resp.json()
        assert data["data"]["total"] == 5
        assert len(data["data"]["items"]) == 3

    def test_list_filter_by_status(self, client):
        client.post("/api/v1/bidding/", json={"title": "意向项目", "bid_status": 1})
        client.post("/api/v1/bidding/", json={"title": "中标项目", "bid_status": 5})
        resp = client.get("/api/v1/bidding/?bid_status=5")
        assert resp.json()["data"]["total"] == 1

    def test_list_search(self, client):
        client.post("/api/v1/bidding/", json={"title": "华为云项目"})
        client.post("/api/v1/bidding/", json={"title": "腾讯项目"})
        resp = client.get("/api/v1/bidding/?search=华为")
        assert resp.json()["data"]["total"] == 1

    def test_get_by_id(self, client):
        r = client.post("/api/v1/bidding/", json={"title": "详情测试"})
        bid_id = r.json()["data"]["id"]
        resp = client.get(f"/api/v1/bidding/{bid_id}")
        assert resp.json()["data"]["title"] == "详情测试"

    def test_get_not_found(self, client):
        resp = client.get("/api/v1/bidding/99999")
        assert resp.status_code == 404

    def test_update(self, client):
        r = client.post("/api/v1/bidding/", json={"title": "更新前"})
        bid_id = r.json()["data"]["id"]
        resp = client.put(f"/api/v1/bidding/{bid_id}", json={"title": "更新后"})
        assert resp.json()["data"]["title"] == "更新后"

    def test_update_status_transition_valid(self, client):
        r = client.post("/api/v1/bidding/", json={"title": "状态", "bid_status": 1})
        bid_id = r.json()["data"]["id"]
        resp = client.put(f"/api/v1/bidding/{bid_id}", json={"bid_status": 2})
        assert resp.json()["data"]["bid_status"] == 2

    def test_update_status_transition_invalid(self, client):
        r = client.post("/api/v1/bidding/", json={"title": "状态", "bid_status": 1})
        bid_id = r.json()["data"]["id"]
        resp = client.put(f"/api/v1/bidding/{bid_id}", json={"bid_status": 5})
        assert resp.status_code == 400

    def test_calendar(self, client):
        future_date = (datetime.now(timezone.utc) + timedelta(days=15)).isoformat()
        client.post("/api/v1/bidding/", json={"title": "即将截止", "bid_deadline": future_date})
        resp = client.get("/api/v1/bidding/calendar/upcoming?days=30")
        assert len(resp.json()["data"]) >= 1
