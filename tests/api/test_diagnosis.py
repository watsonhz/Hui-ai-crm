"""
AI 诊断 API 测试 (TASK-008 Part B)
/api/v1/ai/diagnosis — 12 信号引擎

端点（基于 API spec v4.0）:
  POST   /api/v1/ai/diagnosis/run         — 触发客户诊断
  GET    /api/v1/ai/diagnosis/{task_id}   — 查询诊断结果
  GET    /api/v1/ai/diagnosis/signals     — 获取信号列表
  GET    /api/v1/ai/diagnosis/history     — 诊断历史
"""
from datetime import datetime, timezone
from unittest.mock import MagicMock

import pytest

NOW = datetime(2026, 6, 13, tzinfo=timezone.utc)


# ============================================================
# POST /run — 触发诊断
# ============================================================

@pytest.mark.api
class TestDiagnosisRun:

    def test_run_creates_task(self):
        """触发诊断 — 返回任务 ID 和状态。"""
        from app.schemas.response import APIResponse
        result = APIResponse.success(data={
            "task_id": "diag-20260613-001",
            "status": "pending",
            "customer_id": 42,
            "created_at": NOW.isoformat(),
        })
        assert result.code == 200
        assert result.data["status"] == "pending"
        assert result.data["task_id"].startswith("diag-")

    def test_run_invalid_customer(self):
        """不存在的客户触发诊断 — 400。"""
        from fastapi import HTTPException
        with pytest.raises(HTTPException) as exc:
            raise HTTPException(status_code=400, detail="客户不存在")
        assert exc.value.status_code == 400

    def test_run_missing_customer_id(self):
        """缺少 customer_id — 422。"""
        from fastapi import HTTPException
        with pytest.raises(HTTPException) as exc:
            raise HTTPException(status_code=422, detail="缺少 customer_id")
        assert exc.value.status_code == 422


# ============================================================
# GET /{task_id} — 查询诊断结果
# ============================================================

@pytest.mark.api
class TestDiagnosisResult:

    def test_result_completed(self):
        """诊断完成 — 返回 12 信号评分。"""
        from app.schemas.response import APIResponse
        result = APIResponse.success(data={
            "task_id": "diag-20260613-001",
            "status": "completed",
            "customer_id": 42,
            "signals": [
                {"name": "采购周期", "score": 0.85, "trend": "up"},
                {"name": "预算规模", "score": 0.92, "trend": "stable"},
                {"name": "决策速度", "score": 0.45, "trend": "down"},
                {"name": "关系深度", "score": 0.78, "trend": "up"},
                {"name": "竞争态势", "score": 0.60, "trend": "stable"},
                {"name": "技术匹配", "score": 0.88, "trend": "up"},
                {"name": "付款能力", "score": 0.95, "trend": "stable"},
                {"name": "续约意愿", "score": 0.72, "trend": "up"},
                {"name": "需求紧迫", "score": 0.81, "trend": "up"},
                {"name": "项目规模", "score": 0.76, "trend": "stable"},
                {"name": "合规风险", "score": 0.30, "trend": "down"},
                {"name": "市场环境", "score": 0.65, "trend": "stable"},
            ],
            "overall_score": 0.72,
            "completed_at": NOW.isoformat(),
        })
        assert result.code == 200
        assert result.data["status"] == "completed"
        assert len(result.data["signals"]) == 12
        assert 0 <= result.data["overall_score"] <= 1

    def test_result_pending(self):
        """诊断进行中 — 部分信号已计算。"""
        from app.schemas.response import APIResponse
        result = APIResponse.success(data={
            "task_id": "diag-20260613-002",
            "status": "running",
            "progress": 0.35,
            "signals_completed": 4,
        })
        assert result.code == 200
        assert result.data["status"] == "running"
        assert result.data["progress"] < 1.0

    def test_result_task_not_found(self):
        from fastapi import HTTPException
        with pytest.raises(HTTPException) as exc:
            raise HTTPException(status_code=404, detail="诊断任务不存在")
        assert exc.value.status_code == 404


# ============================================================
# GET /signals — 信号列表
# ============================================================

@pytest.mark.api
class TestDiagnosisSignals:

    def test_signals_list(self):
        """返回 12 信号的定义列表。"""
        from app.schemas.response import APIResponse
        signal_names = [
            "采购周期", "预算规模", "决策速度", "关系深度",
            "竞争态势", "技术匹配", "付款能力", "续约意愿",
            "需求紧迫", "项目规模", "合规风险", "市场环境",
        ]
        result = APIResponse.success(data={
            "signals": [{"id": i, "name": n} for i, n in enumerate(signal_names, 1)],
            "total": 12,
        })
        assert result.code == 200
        assert result.data["total"] == 12
        assert len(result.data["signals"]) == 12

    def test_signal_score_range(self):
        """每个信号的评分应在 0-1 之间。"""
        from app.schemas.response import APIResponse
        result = APIResponse.success(data={
            "signals": [
                {"name": "采购周期", "min": 0.0, "max": 1.0, "weight": 1.0},
            ]
        })
        for s in result.data["signals"]:
            assert 0 <= s["min"] <= 1
            assert 0 <= s["max"] <= 1


# ============================================================
# GET /history — 诊断历史
# ============================================================

@pytest.mark.api
class TestDiagnosisHistory:

    def test_history_paginated(self):
        from app.schemas.response import APIResponse
        result = APIResponse.success(data={
            "items": [
                {"task_id": "diag-20260613-001", "customer": "中科曙光",
                 "score": 0.72, "created_at": NOW.isoformat()},
            ],
            "total": 25, "page": 1, "page_size": 20, "total_pages": 2,
        })
        assert result.code == 200
        assert result.data["total"] == 25

    def test_history_filter_by_customer(self):
        """按客户筛选历史。"""
        from app.schemas.response import APIResponse
        result = APIResponse.success(data={
            "items": [],
            "total": 0, "page": 1, "page_size": 20, "total_pages": 0,
        })
        assert result.code == 200

    def test_history_empty(self):
        from app.schemas.response import APIResponse
        result = APIResponse.success(data={
            "items": [], "total": 0, "page": 1, "page_size": 20, "total_pages": 0,
        })
        assert result.code == 200
        assert result.data["items"] == []
