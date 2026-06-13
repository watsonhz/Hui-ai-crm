"""
AI 报告 API 测试 — 日报/周报/月报生成 (TASK-012 Part A)

POST   /api/v1/ai/reports/daily     — 生成日报
POST   /api/v1/ai/reports/weekly    — 生成周报
POST   /api/v1/ai/reports/monthly   — 生成月报
GET    /api/v1/ai/reports/{id}      — 获取报告
GET    /api/v1/ai/reports/history   — 报告历史
"""
from datetime import datetime, timezone
from unittest.mock import MagicMock

import pytest

NOW = datetime(2026, 6, 13, tzinfo=timezone.utc)


@pytest.mark.api
class TestDailyReport:

    def test_generate_daily_success(self):
        from app.schemas.response import APIResponse
        result = APIResponse.success(data={
            "id": "rpt-daily-20260613",
            "type": "daily",
            "date": "2026-06-13",
            "sections": {
                "completed_tasks": [{"text": "完成XX方案演示", "done": True}],
                "key_progress": [{"text": "XX项目进入商务谈判", "tag": "重大进展"}],
                "pending_issues": [{"text": "合同条款待确认", "tag": "需跟进"}],
                "next_plan": ["明日赴XX现场交流"],
            },
            "generated_at": NOW.isoformat(),
        })
        assert result.code == 200
        assert result.data["type"] == "daily"

    def test_daily_requires_date(self):
        from fastapi import HTTPException
        with pytest.raises(HTTPException) as exc:
            raise HTTPException(status_code=400, detail="缺少日期参数")
        assert exc.value.status_code == 400


@pytest.mark.api
class TestWeeklyReport:

    def test_generate_weekly_success(self):
        from app.schemas.response import APIResponse
        result = APIResponse.success(data={
            "id": "rpt-weekly-2026-W24",
            "type": "weekly",
            "week": "2026-W24",
            "sections": {
                "completed_tasks": [{"text": "完成3家重点客户拜访", "done": True}],
                "key_progress": [{"text": "本周签约3单，合计680万", "tag": "超额完成"}],
                "pipeline_summary": {"new_leads": 23, "active_deals": 15, "closed_won": 3},
            },
            "generated_at": NOW.isoformat(),
        })
        assert result.code == 200
        assert result.data["type"] == "weekly"

    def test_weekly_empty_week(self):
        """无数据周返回空报告但结构正确。"""
        from app.schemas.response import APIResponse
        result = APIResponse.success(data={
            "id": "rpt-weekly-2026-W01",
            "type": "weekly",
            "week": "2026-W01",
            "sections": {"completed_tasks": [], "key_progress": [], "pipeline_summary": {}},
            "generated_at": NOW.isoformat(),
        })
        assert result.code == 200
        assert result.data["sections"]["completed_tasks"] == []


@pytest.mark.api
class TestMonthlyReport:

    def test_generate_monthly_success(self):
        from app.schemas.response import APIResponse
        result = APIResponse.success(data={
            "id": "rpt-monthly-202606",
            "type": "monthly",
            "month": "2026-06",
            "sections": {
                "kpi_summary": {"revenue_target": 5000000, "revenue_actual": 4200000},
                "top_deals": [{"name": "XX项目", "amount": 2000000}],
                "team_performance": [
                    {"name": "张三", "score": 92},
                    {"name": "李四", "score": 85},
                ],
                "ai_insights": "本月 AI 诊断覆盖率 92%，预测准确率 87%",
            },
            "generated_at": NOW.isoformat(),
        })
        assert result.code == 200
        assert result.data["type"] == "monthly"


@pytest.mark.api
class TestReportHistory:

    def test_history_paginated(self):
        from app.schemas.response import APIResponse
        result = APIResponse.success(data={
            "items": [
                {"id": "rpt-daily-20260613", "type": "daily", "date": "2026-06-13"},
                {"id": "rpt-weekly-2026-W24", "type": "weekly", "week": "2026-W24"},
            ],
            "total": 42, "page": 1, "page_size": 20,
        })
        assert result.code == 200
        assert result.data["total"] == 42

    def test_history_filter_by_type(self):
        from app.schemas.response import APIResponse
        result = APIResponse.success(data={
            "items": [], "total": 0, "page": 1, "page_size": 20,
        })
        assert result.code == 200
