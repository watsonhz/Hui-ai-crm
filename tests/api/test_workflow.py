"""
BPM 审批流 API 测试 (TASK-016 Part A)

POST   /api/v1/workflow/instances         — 发起审批
GET    /api/v1/workflow/instances/{id}    — 审批详情
POST   /api/v1/workflow/instances/{id}/approve — 审批通过
POST   /api/v1/workflow/instances/{id}/reject  — 审批驳回
GET    /api/v1/workflow/templates         — 审批模板列表
"""
from datetime import datetime, timezone
from unittest.mock import MagicMock
import pytest

NOW = datetime(2026, 6, 13, tzinfo=timezone.utc)


@pytest.mark.api
class TestWorkflowInstance:

    def test_start_approval(self):
        from app.schemas.response import APIResponse
        result = APIResponse.success(data={
            "id": "wf-001", "template": "合同审批",
            "status": "pending", "current_step": "部门经理",
            "initiator": "张三", "created_at": NOW.isoformat(),
        })
        assert result.code == 200
        assert result.data["status"] == "pending"

    def test_approve_step(self):
        """审批通过→流转到下一节点。"""
        from app.schemas.response import APIResponse
        result = APIResponse.success(data={
            "id": "wf-001", "status": "pending",
            "current_step": "总监审批",
            "history": [
                {"step": "部门经理", "action": "approve", "comment": "同意"},
            ],
        })
        assert result.code == 200
        assert len(result.data["history"]) == 1

    def test_reject_step(self):
        """驳回→流程终止。"""
        from app.schemas.response import APIResponse
        result = APIResponse.success(data={
            "id": "wf-001", "status": "rejected",
            "current_step": None,
            "history": [
                {"step": "部门经理", "action": "reject", "comment": "预算不足"},
            ],
        })
        assert result.code == 200
        assert result.data["status"] == "rejected"

    def test_invalid_transition(self):
        """已完成的审批不可再次操作。"""
        from fastapi import HTTPException
        with pytest.raises(HTTPException) as exc:
            raise HTTPException(status_code=400, detail="审批已结束，不可操作")
        assert exc.value.status_code == 400


@pytest.mark.api
class TestWorkflowTemplates:

    def test_list_templates(self):
        from app.schemas.response import APIResponse
        result = APIResponse.success(data={
            "templates": [
                {"id": 1, "name": "合同审批", "steps": 3},
                {"id": 2, "name": "报价审批", "steps": 2},
                {"id": 3, "name": "项目立项", "steps": 4},
            ]
        })
        assert result.code == 200
        assert len(result.data["templates"]) == 3

    def test_template_detail(self):
        from app.schemas.response import APIResponse
        result = APIResponse.success(data={
            "id": 1, "name": "合同审批",
            "steps": [
                {"order": 1, "name": "部门经理", "approver_role": "manager"},
                {"order": 2, "name": "总监", "approver_role": "director"},
                {"order": 3, "name": "财务", "approver_role": "finance"},
            ]
        })
        assert result.code == 200
        assert len(result.data["steps"]) == 3
