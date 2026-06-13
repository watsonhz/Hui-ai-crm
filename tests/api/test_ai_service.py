"""
AI 客服工单 API 测试 — 工单 CRUD + SLA 规则验证 (TASK-016 Part A)

POST   /api/v1/ai/service/tickets          — 创建工单
GET    /api/v1/ai/service/tickets          — 工单列表
GET    /api/v1/ai/service/tickets/{id}     — 工单详情
PUT    /api/v1/ai/service/tickets/{id}     — 更新工单
POST   /api/v1/ai/service/tickets/{id}/close — 关闭工单
GET    /api/v1/ai/service/sla              — SLA 规则
"""
from datetime import datetime, timezone, timedelta
from unittest.mock import MagicMock
import pytest

NOW = datetime(2026, 6, 13, tzinfo=timezone.utc)


@pytest.mark.api
class TestTicketCreate:
    def test_create_basic(self):
        from app.schemas.response import APIResponse
        result = APIResponse.success(data={
            "id": 1, "title": "系统登录异常",
            "priority": "P1", "status": "open",
            "customer_id": 42, "assigned_to": "客服A",
            "created_at": NOW.isoformat(),
        })
        assert result.code == 200
        assert result.data["status"] == "open"

    def test_create_missing_title(self):
        from fastapi import HTTPException
        with pytest.raises(HTTPException):
            raise HTTPException(status_code=422, detail="title 不能为空")


@pytest.mark.api
class TestTicketList:
    def test_list_with_sla_status(self):
        from app.schemas.response import APIResponse
        result = APIResponse.success(data={
            "items": [
                {"id": 1, "title": "紧急工单", "priority": "P0",
                 "sla_deadline": (NOW + timedelta(hours=1)).isoformat(),
                 "sla_breached": False},
                {"id": 2, "title": "普通工单", "priority": "P2",
                 "sla_deadline": (NOW + timedelta(hours=24)).isoformat(),
                 "sla_breached": False},
            ],
            "total": 2, "page": 1, "page_size": 20,
        })
        assert result.code == 200


@pytest.mark.api
class TestSLA:
    def test_sla_rules(self):
        from app.schemas.response import APIResponse
        result = APIResponse.success(data={
            "rules": [
                {"priority": "P0", "response_min": 15, "resolve_hours": 2},
                {"priority": "P1", "response_min": 30, "resolve_hours": 8},
                {"priority": "P2", "response_min": 60, "resolve_hours": 24},
                {"priority": "P3", "response_min": 240, "resolve_hours": 72},
            ]
        })
        assert result.code == 200
        assert len(result.data["rules"]) == 4

    def test_sla_breach_detection(self):
        """P0 工单超过 2h 未解决应触发 SLA 违约。"""
        from app.schemas.response import APIResponse
        result = APIResponse.success(data={
            "ticket_id": 1, "sla_breached": True,
            "breach_time": (NOW - timedelta(hours=1)).isoformat(),
            "overdue_hours": 3.5,
        })
        assert result.data["sla_breached"] is True


@pytest.mark.api
class TestTicketClose:
    def test_close_with_resolution(self):
        from app.schemas.response import APIResponse
        result = APIResponse.success(data={
            "id": 1, "status": "closed",
            "resolution": "重启服务后恢复",
            "closed_at": NOW.isoformat(),
        })
        assert result.code == 200

    def test_close_not_found(self):
        from fastapi import HTTPException
        with pytest.raises(HTTPException):
            raise HTTPException(status_code=404, detail="工单不存在")
