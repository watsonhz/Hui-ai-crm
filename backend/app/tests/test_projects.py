"""项目管理 API 测试 —— CRUD + 阶段前进 + 看板视图。"""

from datetime import date, timedelta

import pytest
from fastapi.testclient import TestClient


def _create_project(client: TestClient, **overrides) -> dict:
    """快捷创建项目，返回响应 data。"""
    payload = {
        "project_name": "测试项目",
        "customer_name": "测试客户",
        "pm_name": "张三",
        "start_date": "2026-06-01",
        "expected_end_date": "2026-12-31",
        "amount": "500000.00",
        **overrides,
    }
    resp = client.post("/api/v1/projects", json=payload)
    assert resp.status_code == 201, resp.text
    return resp.json()["data"]


class TestProjectCRUD:
    """CRUD 基础测试。"""

    def test_create(self, client: TestClient):
        data = _create_project(client, project_name="智慧城市项目")
        assert data["project_name"] == "智慧城市项目"
        assert data["stage"] == "初步接洽"
        assert data["progress"] == 0
        assert data["pm_name"] == "张三"
        assert data["id"] is not None

    def test_create_invalid_stage(self, client: TestClient):
        resp = client.post("/api/v1/projects", json={
            "project_name": "X", "customer_name": "C", "pm_name": "P",
            "start_date": "2026-06-01", "expected_end_date": "2026-12-31",
            "stage": "不存在阶段",
        })
        assert resp.status_code == 422

    def test_create_invalid_progress(self, client: TestClient):
        resp = client.post("/api/v1/projects", json={
            "project_name": "X", "customer_name": "C", "pm_name": "P",
            "start_date": "2026-06-01", "expected_end_date": "2026-12-31",
            "progress": 150,
        })
        assert resp.status_code == 422

    def test_list(self, client: TestClient):
        _create_project(client, project_name="A")
        _create_project(client, project_name="B")
        resp = client.get("/api/v1/projects?page=1&page_size=10")
        assert resp.status_code == 200
        d = resp.json()["data"]
        assert d["total"] == 2
        assert len(d["items"]) == 2

    def test_list_filter_stage(self, client: TestClient):
        _create_project(client)
        resp = client.get("/api/v1/projects?stage=初步接洽")
        assert resp.json()["data"]["total"] >= 1
        resp = client.get("/api/v1/projects?stage=维保服务")
        assert resp.json()["data"]["total"] == 0

    def test_list_filter_pm(self, client: TestClient):
        _create_project(client, pm_name="李四")
        resp = client.get("/api/v1/projects?pm_name=李四")
        assert resp.json()["data"]["total"] >= 1

    def test_get_by_id(self, client: TestClient):
        data = _create_project(client, project_name="详情项目")
        resp = client.get(f"/api/v1/projects/{data['id']}")
        assert resp.status_code == 200
        assert resp.json()["data"]["project_name"] == "详情项目"

    def test_get_not_found(self, client: TestClient):
        resp = client.get("/api/v1/projects/99999")
        assert resp.status_code == 404

    def test_update(self, client: TestClient):
        data = _create_project(client)
        resp = client.put(f"/api/v1/projects/{data['id']}", json={
            "project_name": "改名项目", "progress": 50,
        })
        assert resp.status_code == 200
        assert resp.json()["data"]["project_name"] == "改名项目"
        assert resp.json()["data"]["progress"] == 50

    def test_soft_delete(self, client: TestClient):
        data = _create_project(client)
        del_resp = client.delete(f"/api/v1/projects/{data['id']}")
        assert del_resp.status_code == 200
        get_resp = client.get(f"/api/v1/projects/{data['id']}")
        assert get_resp.status_code == 404


class TestProjectStageAdvance:
    """阶段前进测试。"""

    def test_forward_chain(self, client: TestClient):
        """测试完整 12 阶段正向链路。"""
        data = _create_project(client)
        pid = data["id"]

        # 从初步接洽一路推进到维保服务
        stages = [
            "需求分析", "方案演示", "报价", "商务谈判", "合同签订",
            "项目启动", "设计开发", "测试验收", "上线部署", "项目交付", "维保服务",
        ]
        for stage in stages:
            resp = client.put(
                f"/api/v1/projects/{pid}/stage",
                json={"new_stage": stage},
            )
            assert resp.status_code == 200, f"推进到 {stage}: {resp.text}"
            assert resp.json()["data"]["stage"] == stage

    def test_backward_rejected(self, client: TestClient):
        """不允许回退阶段。"""
        data = _create_project(client)
        pid = data["id"]

        client.put(f"/api/v1/projects/{pid}/stage", json={"new_stage": "需求分析"})
        client.put(f"/api/v1/projects/{pid}/stage", json={"new_stage": "方案演示"})

        # 试图回退到需求分析
        resp = client.put(f"/api/v1/projects/{pid}/stage", json={"new_stage": "需求分析"})
        assert resp.status_code == 400

    def test_same_stage_rejected(self, client: TestClient):
        """不允许停留在同一阶段（target_idx <= current_idx 判断）。"""
        data = _create_project(client)
        pid = data["id"]
        resp = client.put(f"/api/v1/projects/{pid}/stage", json={"new_stage": "初步接洽"})
        assert resp.status_code == 400

    def test_skip_stage(self, client: TestClient):
        """允许跳阶段：初步接洽 -> 报价（跳过两个）。"""
        data = _create_project(client)
        pid = data["id"]
        resp = client.put(f"/api/v1/projects/{pid}/stage", json={"new_stage": "报价"})
        assert resp.status_code == 200
        assert resp.json()["data"]["stage"] == "报价"

    def test_stage_not_found_project(self, client: TestClient):
        resp = client.put("/api/v1/projects/99999/stage", json={"new_stage": "需求分析"})
        assert resp.status_code == 404


class TestProjectKanban:
    """看板视图测试。"""

    def test_kanban_empty(self, client: TestClient):
        resp = client.get("/api/v1/projects/kanban")
        assert resp.status_code == 200
        columns = resp.json()["data"]["columns"]
        assert len(columns) == 12
        assert all(c["count"] == 0 for c in columns)

    def test_kanban_with_projects(self, client: TestClient):
        _create_project(client, project_name="A")
        _create_project(client, project_name="B")

        resp = client.get("/api/v1/projects/kanban")
        assert resp.status_code == 200
        columns = resp.json()["data"]["columns"]
        first_col = columns[0]
        assert first_col["stage"] == "初步接洽"
        assert first_col["count"] == 2
        assert len(first_col["items"]) == 2

    def test_kanban_grouped_correctly(self, client: TestClient):
        """确认不同阶段的项目出现在对应列中。"""
        data = _create_project(client, project_name="保持初接")
        # 推进一个到需求分析
        _create_project(client, project_name="推进项目")
        data2 = _create_project(client, project_name="推进项目2")
        client.put(f"/api/v1/projects/{data2['id']}/stage", json={"new_stage": "需求分析"})

        resp = client.get("/api/v1/projects/kanban")
        columns = resp.json()["data"]["columns"]

        # 第一列: 初步接洽
        assert columns[0]["stage"] == "初步接洽"
        assert columns[0]["count"] == 2  # data + 保持初接

        # 第二列: 需求分析
        assert columns[1]["stage"] == "需求分析"
        assert columns[1]["count"] == 1
