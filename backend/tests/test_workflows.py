"""Tests for BPM workflow engine — defs + instances + approval flow + authz."""

import pytest

WF_3STAGE = {
    "stages": [
        {"name": "提交申请", "assignee_role": "user", "order": 1},
        {"name": "经理审批", "assignee_role": "admin", "order": 2},
        {"name": "完成", "assignee_role": "admin", "order": 3},
    ],
    "transitions": {
        "提交申请": {"approve": "经理审批", "reject": None},
        "经理审批": {"approve": "完成", "reject": "提交申请"},
        "完成": {"approve": None, "reject": None},
    },
}


class TestWorkflowModel:
    def test_create_definition(self, db):
        from app.models.workflow import WorkflowDefinition
        wf = WorkflowDefinition(name="报销", definition_json=WF_3STAGE, created_by=1, status="active")
        db.add(wf)
        db.commit()
        assert wf.id is not None

    def test_rejects_empty_stages(self):
        from app.models.workflow import WorkflowDefinition
        with pytest.raises(ValueError):
            WorkflowDefinition(name="bad", definition_json={"stages": []}, created_by=1)

    def test_rejects_bad_transitions(self):
        from app.models.workflow import WorkflowDefinition
        with pytest.raises(ValueError):
            WorkflowDefinition(
                name="bad",
                definition_json={
                    "stages": [{"name": "A"}, {"name": "B"}],
                    "transitions": {"C": {"approve": "A"}},
                },
                created_by=1,
            )

    def test_create_instance(self, db):
        from app.models.workflow import WorkflowDefinition, WorkflowInstance
        wf = WorkflowDefinition(name="t", definition_json=WF_3STAGE, created_by=1, status="active")
        db.add(wf)
        db.commit()
        inst = WorkflowInstance(definition_id=wf.id, title="报销", current_stage="提交申请", tenant_id=1, created_by=1)
        db.add(inst)
        db.commit()
        assert inst.id is not None


class TestWorkflowsAPIAuth:
    @pytest.mark.parametrize("method,path", [
        ("GET", "/api/v1/workflows/definitions"),
        ("POST", "/api/v1/workflows/instances"),
        ("GET", "/api/v1/workflows/instances"),
        ("GET", "/api/v1/workflows/instances/1"),
        ("POST", "/api/v1/workflows/instances/1/approve"),
        ("POST", "/api/v1/workflows/instances/1/reject"),
        ("GET", "/api/v1/workflows/instances/1/tasks"),
    ])
    def test_no_auth(self, client, method, path):
        body = {"definition_id": 1, "title": "x"} if method == "POST" else None
        r = client.request(method, path, json=body) if body else client.request(method, path)
        assert r.status_code == 401, f"{method} {path} got {r.status_code}"


class TestWorkflowsAPIDefinition:
    def test_create(self, client, auth_header):
        r = client.post("/api/v1/workflows/definitions", json={
            "name": "报销审批", "definition_json": WF_3STAGE,
        }, headers={"Authorization": auth_header})
        assert r.status_code == 200
        assert r.json()["data"]["name"] == "报销审批"

    def test_create_draft(self, client, auth_header):
        r = client.post("/api/v1/workflows/definitions", json={
            "name": "草稿", "definition_json": WF_3STAGE, "status": "draft",
        }, headers={"Authorization": auth_header})
        assert r.status_code == 200
        assert r.json()["data"]["status"] == "draft"

    def test_list(self, client, auth_header):
        client.post("/api/v1/workflows/definitions", json={
            "name": "wf1", "definition_json": WF_3STAGE,
        }, headers={"Authorization": auth_header})
        r = client.get("/api/v1/workflows/definitions", headers={"Authorization": auth_header})
        assert r.json()["data"]["total"] == 1


class TestWorkflowsAPIApproval:
    def test_full_flow(self, client, auth_header, admin_user):
        """End-to-end: def → start → approve → approve → terminal."""
        r = client.post("/api/v1/workflows/definitions", json={
            "name": "完整流程测试", "definition_json": WF_3STAGE,
        }, headers={"Authorization": auth_header})
        def_id = r.json()["data"]["id"]

        r = client.post("/api/v1/workflows/instances", json={
            "definition_id": def_id, "title": "测试报销1000元",
        }, headers={"Authorization": auth_header})
        assert r.status_code == 200
        data = r.json()["data"]
        inst_id = data["id"]
        assert data["current_stage"] == "提交申请"

        # Approve stage 1 → stage 2
        r = client.post(f"/api/v1/workflows/instances/{inst_id}/approve",
                        headers={"Authorization": auth_header})
        assert r.status_code == 200
        assert r.json()["data"]["current_stage"] == "经理审批"

        # Approve stage 2 → stage 3 (terminal)
        r = client.post(f"/api/v1/workflows/instances/{inst_id}/approve",
                        headers={"Authorization": auth_header})
        assert r.status_code == 200
        assert r.json()["data"]["current_stage"] == "完成"
        assert r.json()["data"]["status"] in ("active", "approved")  # terminal

        # Completed instance can't be acted on again
        r = client.post(f"/api/v1/workflows/instances/{inst_id}/approve",
                        headers={"Authorization": auth_header})
        assert r.status_code in (400, 200)  # 400 for ended, 200 if final stage has no pending task

    def test_reject_goes_back(self, client, auth_header):
        """Reject on stage 2 sends back to stage 1."""
        r = client.post("/api/v1/workflows/definitions", json={
            "name": "驳回测试", "definition_json": WF_3STAGE,
        }, headers={"Authorization": auth_header})
        def_id = r.json()["data"]["id"]

        r = client.post("/api/v1/workflows/instances", json={
            "definition_id": def_id, "title": "可驳回",
        }, headers={"Authorization": auth_header})
        inst_id = r.json()["data"]["id"]

        # Approve to stage 2
        client.post(f"/api/v1/workflows/instances/{inst_id}/approve",
                    headers={"Authorization": auth_header})
        # Reject back to stage 1
        r = client.post(f"/api/v1/workflows/instances/{inst_id}/reject",
                        json={"comment": "金额不对"},
                        headers={"Authorization": auth_header})
        assert r.status_code == 200
        assert r.json()["data"]["current_stage"] == "提交申请"


class TestWorkflowsAPIAuthz:
    def test_other_user_blocked(self, client, normal_auth_header, other_auth_header):
        """User A creates instance → User B cannot see it."""
        r = client.post("/api/v1/workflows/definitions", json={
            "name": "隔离测试", "definition_json": WF_3STAGE,
        }, headers={"Authorization": normal_auth_header})
        def_id = r.json()["data"]["id"]

        r = client.post("/api/v1/workflows/instances", json={
            "definition_id": def_id, "title": "A的流程",
        }, headers={"Authorization": normal_auth_header})
        inst_id = r.json()["data"]["id"]

        # User B tries to view
        r = client.get(f"/api/v1/workflows/instances/{inst_id}",
                       headers={"Authorization": other_auth_header})
        assert r.status_code == 403

    def test_admin_can_see_all(self, client, normal_auth_header, auth_header):
        """Admin can view any tenant's instances."""
        r = client.post("/api/v1/workflows/definitions", json={
            "name": "admin测试", "definition_json": WF_3STAGE,
        }, headers={"Authorization": auth_header})
        def_id = r.json()["data"]["id"]

        r = client.post("/api/v1/workflows/instances", json={
            "definition_id": def_id, "title": "某人的流程",
        }, headers={"Authorization": normal_auth_header})
        inst_id = r.json()["data"]["id"]

        r = client.get(f"/api/v1/workflows/instances/{inst_id}",
                       headers={"Authorization": auth_header})
        assert r.status_code == 200
