"""投标管理 API 测试 —— CRUD + 9阶段状态机 + 日历视图。"""

from datetime import date, timedelta

import pytest
from fastapi.testclient import TestClient


def _create(client: TestClient, **overrides) -> dict:
    """快捷创建投标项目，返回响应 data。"""
    payload = {
        "project_name": "测试项目",
        "customer_name": "测试客户",
        "amount": "100000.00",
        "bid_deadline": "2026-12-31",
        **overrides,
    }
    resp = client.post("/api/v1/bidding", json=payload)
    assert resp.status_code == 201, resp.text
    return resp.json()["data"]


class TestBiddingCRUD:
    """CRUD 基础测试。"""

    def test_create(self, client: TestClient):
        data = _create(client, project_name="智慧园区投标")
        assert data["project_name"] == "智慧园区投标"
        assert data["status"] == "线索"
        assert data["probability"] == 0
        assert data["id"] is not None

    def test_create_invalid_status(self, client: TestClient):
        resp = client.post("/api/v1/bidding", json={
            "project_name": "X", "customer_name": "C",
            "amount": "1.00", "bid_deadline": "2026-12-31",
            "status": "不存在",
        })
        assert resp.status_code == 422

    def test_create_negative_amount(self, client: TestClient):
        resp = client.post("/api/v1/bidding", json={
            "project_name": "X", "customer_name": "C",
            "amount": "-1.00", "bid_deadline": "2026-12-31",
        })
        assert resp.status_code == 422

    def test_list(self, client: TestClient):
        _create(client, project_name="A")
        _create(client, project_name="B")
        resp = client.get("/api/v1/bidding?page=1&page_size=10")
        assert resp.status_code == 200
        d = resp.json()["data"]
        assert d["total"] == 2
        assert len(d["items"]) == 2

    def test_list_filter_status(self, client: TestClient):
        _create(client)
        resp = client.get("/api/v1/bidding?status=线索")
        assert resp.json()["data"]["total"] >= 1
        resp = client.get("/api/v1/bidding?status=中标")
        assert resp.json()["data"]["total"] == 0

    def test_list_filter_customer(self, client: TestClient):
        _create(client, customer_name="华为技术")
        resp = client.get("/api/v1/bidding?customer_name=华为")
        assert resp.json()["data"]["total"] >= 1

    def test_get_by_id(self, client: TestClient):
        data = _create(client, project_name="详情")
        resp = client.get(f"/api/v1/bidding/{data['id']}")
        assert resp.status_code == 200
        assert resp.json()["data"]["project_name"] == "详情"

    def test_get_not_found(self, client: TestClient):
        resp = client.get("/api/v1/bidding/99999")
        assert resp.status_code == 404

    def test_update_fields(self, client: TestClient):
        data = _create(client)
        resp = client.put(f"/api/v1/bidding/{data['id']}", json={
            "project_name": "改名", "probability": 80,
        })
        assert resp.status_code == 200
        assert resp.json()["data"]["project_name"] == "改名"
        assert resp.json()["data"]["probability"] == 80

    def test_soft_delete(self, client: TestClient):
        data = _create(client)
        del_resp = client.delete(f"/api/v1/bidding/{data['id']}")
        assert del_resp.status_code == 200
        get_resp = client.get(f"/api/v1/bidding/{data['id']}")
        assert get_resp.status_code == 404


class TestBiddingStatusTransitions:
    """9 阶段状态机测试。"""

    def test_full_forward_chain(self, client: TestClient):
        """完整正向链路: 线索→商机确认→方案设计→投标中→商务谈判→中标→项目交付→维保。"""
        data = _create(client)
        bid_id = data["id"]

        chain = ["商机确认", "方案设计", "投标中", "商务谈判", "中标", "项目交付", "维保"]
        for status in chain:
            resp = client.put(
                f"/api/v1/bidding/{bid_id}",
                json={"new_status": status},
            )
            assert resp.status_code == 200, f"{status}: {resp.text}"
            assert resp.json()["data"]["status"] == status

    def test_bid_to_loss_transition(self, client: TestClient):
        """投标中 -> 丢标 路径。"""
        data = _create(client)
        bid_id = data["id"]

        # 线索 -> 商机确认 -> 方案设计 -> 投标中
        for status in ["商机确认", "方案设计", "投标中"]:
            client.put(f"/api/v1/bidding/{bid_id}", json={"new_status": status})

        # 投标中 -> 丢标
        resp = client.put(f"/api/v1/bidding/{bid_id}", json={"new_status": "丢标"})
        assert resp.status_code == 200
        assert resp.json()["data"]["status"] == "丢标"

    def test_negotiation_to_loss(self, client: TestClient):
        """商务谈判 -> 丢标 路径。"""
        data = _create(client)
        bid_id = data["id"]

        for status in ["商机确认", "方案设计", "投标中", "商务谈判"]:
            client.put(f"/api/v1/bidding/{bid_id}", json={"new_status": status})

        resp = client.put(f"/api/v1/bidding/{bid_id}", json={"new_status": "丢标"})
        assert resp.status_code == 200

    def test_skip_stage_rejected(self, client: TestClient):
        """跨阶段跳转应被拒绝: 线索 -> 投标中。"""
        data = _create(client)
        bid_id = data["id"]
        resp = client.put(f"/api/v1/bidding/{bid_id}", json={"new_status": "投标中"})
        assert resp.status_code == 400

    def test_terminal_loss_no_transition(self, client: TestClient):
        """丢标是终态，不能再转其他。"""
        data = _create(client)
        bid_id = data["id"]
        for status in ["商机确认", "方案设计", "投标中", "丢标"]:
            client.put(f"/api/v1/bidding/{bid_id}", json={"new_status": status})

        resp = client.put(f"/api/v1/bidding/{bid_id}", json={"new_status": "项目交付"})
        assert resp.status_code == 400

    def test_terminal_maintenance_no_transition(self, client: TestClient):
        """维保是终态，不能再转其他。"""
        data = _create(client)
        bid_id = data["id"]
        for status in ["商机确认", "方案设计", "投标中", "商务谈判", "中标", "项目交付", "维保"]:
            client.put(f"/api/v1/bidding/{bid_id}", json={"new_status": status})

        resp = client.put(f"/api/v1/bidding/{bid_id}", json={"new_status": "中标"})
        assert resp.status_code == 400

    def test_backward_transition_rejected(self, client: TestClient):
        """不允许回退: 方案设计 -> 商机确认。"""
        data = _create(client)
        bid_id = data["id"]
        client.put(f"/api/v1/bidding/{bid_id}", json={"new_status": "商机确认"})
        client.put(f"/api/v1/bidding/{bid_id}", json={"new_status": "方案设计"})

        resp = client.put(f"/api/v1/bidding/{bid_id}", json={"new_status": "商机确认"})
        assert resp.status_code == 400


class TestBiddingCalendar:
    """日历视图测试。"""

    def test_calendar_future_items(self, client: TestClient):
        tomorrow = (date.today() + timedelta(days=1)).isoformat()
        _create(client, project_name="明天截止", bid_deadline=tomorrow)

        resp = client.get("/api/v1/bidding/calendar?days=30")
        assert resp.status_code == 200
        items = resp.json()["data"]["items"]
        assert len(items) >= 1
        assert items[0]["days_left"] == 1

    def test_calendar_excludes_past(self, client: TestClient):
        yesterday = (date.today() - timedelta(days=1)).isoformat()
        _create(client, project_name="已过期", bid_deadline=yesterday)

        resp = client.get("/api/v1/bidding/calendar?days=30")
        items = resp.json()["data"]["items"]
        # 过期的投标不应出现在日历中
        names = [it["project_name"] for it in items]
        assert "已过期" not in names
