"""Tests for projects.py — models + all 6 API endpoints with auth."""

import pytest
from datetime import date

from app.models.project import Project, STAGE_MAP, VALID_STAGE_TRANSITIONS


# ── Model tests ──────────────────────────────────────────────────────────────


class TestProjectModel:
    def test_create_minimal(self, db):
        p = Project(name="测试项目", stage=1)
        db.add(p)
        db.commit()
        db.refresh(p)
        assert p.id is not None
        assert p.stage == 1
        assert p.deleted_at is None

    def test_create_with_all_fields(self, db):
        p = Project(
            name="政企大客户CRM",
            description="政府大客户关系管理系统",
            stage=3,
            start_date=date(2026, 1, 1),
            end_date=date(2026, 12, 31),
            budget=2000000.00,
            actual_cost=500000.00,
            manager_id=1,
            org_id=1,
        )
        db.add(p)
        db.commit()
        assert p.budget == 2000000.00
        assert p.actual_cost == 500000.00

    def test_invalid_stage_raises(self):
        p = Project(name="test")
        with pytest.raises(ValueError, match="无效的项目阶段"):
            p.stage = 99

    def test_all_valid_stages(self):
        p = Project(name="test")
        for stage in STAGE_MAP:
            p.stage = stage

    def test_stage_transitions(self):
        """线索→商机 ok, 线索→合同 denied."""
        p = Project(name="test", stage=1)
        assert p.can_transition_to(2) is True
        assert p.can_transition_to(12) is True
        assert p.can_transition_to(7) is False

<<<<<<< HEAD
    def test_terminal_stage_no_transitions(self):
        """结项(12)不可再转换."""
        p = Project(name="test", stage=12)
        for stage in STAGE_MAP:
            assert p.can_transition_to(stage) is False
=======

class TestProjectsAPI:
    def test_create(self, client):
        resp = client.post("/api/v1/projects/", json={"name": "新项目", "stage": 1})
        assert resp.json()["data"]["name"] == "新项目"
>>>>>>> 662f12488696422c660a7b9ff57a0f880cf8e5a8

    def test_linear_pipeline(self):
        """订单流水线: 1→2→3→4→5→6→7→8→9→10→11→12 each step valid."""
        p = Project(name="pipeline", stage=1)
        for next_stage in range(2, 13):
            assert p.can_transition_to(next_stage) is True or next_stage == 12
            if p.can_transition_to(next_stage):
                p.stage = next_stage


# ── 401 Unauthorized ─────────────────────────────────────────────────────────

class TestProjectsAPIAuth:
    def test_create_no_auth(self, client):
        r = client.post("/api/v1/projects/", json={"name": "x"})
        assert r.status_code == 401

    def test_list_no_auth(self, client):
        r = client.get("/api/v1/projects/")
        assert r.status_code == 401

    def test_get_no_auth(self, client):
        r = client.get("/api/v1/projects/1")
        assert r.status_code == 401

    def test_update_no_auth(self, client):
        r = client.put("/api/v1/projects/1", json={"name": "x"})
        assert r.status_code == 401

    def test_update_stage_no_auth(self, client):
        r = client.put("/api/v1/projects/1/stage", json={"stage": 2})
        assert r.status_code == 401

    def test_kanban_no_auth(self, client):
        r = client.get("/api/v1/projects/board/kanban")
        assert r.status_code == 401


# ── CRUD (authenticated as admin) ────────────────────────────────────────────

class TestProjectsAPICRUD:
    def test_create(self, client, auth_header, admin_user):
        r = client.post("/api/v1/projects/", json={"name": "新项目", "stage": 1},
                        headers={"Authorization": auth_header})
        assert r.status_code == 200
        assert r.json()["data"]["name"] == "新项目"
        assert r.json()["data"]["manager_id"] == admin_user.id

    def test_create_validation_error(self, client, auth_header):
        r = client.post("/api/v1/projects/", json={"name": "x", "stage": 99},
                        headers={"Authorization": auth_header})
        assert r.status_code == 422

    def test_get_by_id(self, client, auth_header):
        r = client.post("/api/v1/projects/", json={"name": "详情"},
                        headers={"Authorization": auth_header})
        pid = r.json()["data"]["id"]
        r = client.get(f"/api/v1/projects/{pid}",
                       headers={"Authorization": auth_header})
        assert r.json()["data"]["name"] == "详情"

    def test_get_not_found(self, client, auth_header):
        r = client.get("/api/v1/projects/99999", headers={"Authorization": auth_header})
        assert r.status_code == 404

    def test_update(self, client, auth_header):
        r = client.post("/api/v1/projects/", json={"name": "旧名称"},
                        headers={"Authorization": auth_header})
        pid = r.json()["data"]["id"]
        r = client.put(f"/api/v1/projects/{pid}", json={"name": "新名称"},
                       headers={"Authorization": auth_header})
        assert r.json()["data"]["name"] == "新名称"

    def test_update_stage_valid(self, client, auth_header):
        r = client.post("/api/v1/projects/", json={"name": "阶段测试", "stage": 1},
                        headers={"Authorization": auth_header})
        pid = r.json()["data"]["id"]
        r = client.put(f"/api/v1/projects/{pid}/stage", json={"stage": 2},
                       headers={"Authorization": auth_header})
        assert r.json()["data"]["stage"] == 2

    def test_update_stage_invalid(self, client, auth_header):
        r = client.post("/api/v1/projects/", json={"name": "跳阶段", "stage": 1},
                        headers={"Authorization": auth_header})
        pid = r.json()["data"]["id"]
        r = client.put(f"/api/v1/projects/{pid}/stage", json={"stage": 7},
                       headers={"Authorization": auth_header})
        assert r.status_code == 400

    def test_update_not_found(self, client, auth_header):
        r = client.put("/api/v1/projects/99999", json={"name": "x"},
                       headers={"Authorization": auth_header})
        assert r.status_code == 404


# ── List / Pagination / Filter ───────────────────────────────────────────────

class TestProjectsAPIList:
    def test_list_empty(self, client, auth_header):
        r = client.get("/api/v1/projects/", headers={"Authorization": auth_header})
        assert r.json()["data"]["items"] == []

    def test_list_pagination(self, client, auth_header):
        for i in range(5):
            client.post("/api/v1/projects/", json={"name": f"项目{i}"},
                        headers={"Authorization": auth_header})
        r = client.get("/api/v1/projects/?page=1&page_size=3",
                       headers={"Authorization": auth_header})
        data = r.json()["data"]
        assert data["total"] == 5
        assert len(data["items"]) == 3

    def test_list_filter_by_stage(self, client, auth_header):
        client.post("/api/v1/projects/", json={"name": "线索", "stage": 1},
                    headers={"Authorization": auth_header})
        client.post("/api/v1/projects/", json={"name": "合同", "stage": 7},
                    headers={"Authorization": auth_header})
        r = client.get("/api/v1/projects/?stage=7",
                       headers={"Authorization": auth_header})
        assert r.json()["data"]["total"] == 1

    def test_list_search(self, client, auth_header):
        client.post("/api/v1/projects/", json={"name": "华为云项目"},
                    headers={"Authorization": auth_header})
        client.post("/api/v1/projects/", json={"name": "腾讯项目"},
                    headers={"Authorization": auth_header})
        r = client.get("/api/v1/projects/?search=华为",
                       headers={"Authorization": auth_header})
        assert r.json()["data"]["total"] == 1

    def test_list_search_like_escape(self, client, auth_header):
        client.post("/api/v1/projects/", json={"name": "普通项目"},
                    headers={"Authorization": auth_header})
        r = client.get("/api/v1/projects/?search=%%",
                       headers={"Authorization": auth_header})
        assert r.json()["data"]["total"] == 0


# ── Kanban ───────────────────────────────────────────────────────────────────

class TestProjectsAPIKanban:
    def test_kanban_all_stages_present(self, client, auth_header):
        r = client.get("/api/v1/projects/board/kanban",
                       headers={"Authorization": auth_header})
        assert r.status_code == 200
        data = r.json()["data"]
        assert len(data) == 12
        stages_found = {d["stage"] for d in data}
        assert stages_found == set(STAGE_MAP.keys())

    def test_kanban_with_projects(self, client, auth_header):
        client.post("/api/v1/projects/", json={"name": "线索项目", "stage": 1},
                    headers={"Authorization": auth_header})
        client.post("/api/v1/projects/", json={"name": "合同项目", "stage": 7},
                    headers={"Authorization": auth_header})
        data = client.get("/api/v1/projects/board/kanban",
                          headers={"Authorization": auth_header}).json()["data"]
        assert [d for d in data if d["stage"] == 1][0]["count"] == 1
        assert [d for d in data if d["stage"] == 7][0]["count"] == 1


# ── Authorization (ownership enforcement) ────────────────────────────────────

class TestProjectsAPIAuthz:
    def test_create_manager_is_current_user(self, client, normal_auth_header, normal_user):
        r = client.post("/api/v1/projects/", json={"name": "我的项目", "stage": 1},
                        headers={"Authorization": normal_auth_header})
        assert r.status_code == 200
        assert r.json()["data"]["manager_id"] == normal_user.id

    def test_create_ignores_provided_manager_id(self, client, normal_auth_header, normal_user):
        r = client.post("/api/v1/projects/",
                        json={"name": "冒充", "stage": 1, "manager_id": 1},
                        headers={"Authorization": normal_auth_header})
        assert r.status_code == 200
        assert r.json()["data"]["manager_id"] == normal_user.id

    def test_update_by_other_user_forbidden(self, client, normal_auth_header, other_auth_header):
        r = client.post("/api/v1/projects/", json={"name": "A的项目"},
                        headers={"Authorization": normal_auth_header})
        pid = r.json()["data"]["id"]
        r = client.put(f"/api/v1/projects/{pid}", json={"name": "B篡改"},
                       headers={"Authorization": other_auth_header})
        assert r.status_code == 403

    def test_update_stage_by_other_user_forbidden(self, client, normal_auth_header, other_auth_header):
        r = client.post("/api/v1/projects/", json={"name": "A的项目", "stage": 1},
                        headers={"Authorization": normal_auth_header})
        pid = r.json()["data"]["id"]
        r = client.put(f"/api/v1/projects/{pid}/stage", json={"stage": 2},
                       headers={"Authorization": other_auth_header})
        assert r.status_code == 403

    def test_update_by_admin_succeeds(self, client, normal_auth_header, auth_header):
        r = client.post("/api/v1/projects/", json={"name": "用户的项目"},
                        headers={"Authorization": normal_auth_header})
        pid = r.json()["data"]["id"]
        r = client.put(f"/api/v1/projects/{pid}", json={"name": "管理员修改"},
                       headers={"Authorization": auth_header})
        assert r.status_code == 200

    def test_update_stage_by_admin_succeeds(self, client, normal_auth_header, auth_header):
        r = client.post("/api/v1/projects/", json={"name": "用户的项目", "stage": 1},
                        headers={"Authorization": normal_auth_header})
        pid = r.json()["data"]["id"]
        r = client.put(f"/api/v1/projects/{pid}/stage", json={"stage": 2},
                       headers={"Authorization": auth_header})
        assert r.status_code == 200
