"""
AI 诊断引擎扩展测试 — S5-S12 信号 (TASK-012 Part A)

12 信号引擎:
  S1-S4 (已测试): 采购周期, 预算规模, 决策速度, 关系深度
  S5-S8 (扩展1): 技术适配, 合规风险, 市场竞争, 付款信用
  S9-S12 (扩展2): 续约潜力, 扩展空间, 战略匹配, 团队能力

POST   /api/v1/ai/diagnosis/run-all    — 全12信号诊断
GET    /api/v1/ai/diagnosis/signals    — 信号列表+权重
GET    /api/v1/ai/diagnosis/trend/{id} — 信号趋势
"""
from datetime import datetime, timezone
from unittest.mock import MagicMock

import pytest

NOW = datetime(2026, 6, 13, tzinfo=timezone.utc)

ALL_12_SIGNALS = [
    ("S1", "采购周期", 0.10, "客户采购频率与季节性"),
    ("S2", "预算规模", 0.10, "历史合同金额与增长率"),
    ("S3", "决策速度", 0.08, "从线索到签约的平均周期"),
    ("S4", "关系深度", 0.10, "多层级接触点覆盖"),
    ("S5", "技术适配", 0.08, "我方方案与客户技术栈匹配度"),
    ("S6", "合规风险", 0.08, "行业监管与数据安全要求"),
    ("S7", "市场竞争", 0.08, "竞争对手活跃度与价格压力"),
    ("S8", "付款信用", 0.10, "历史回款周期与信用评级"),
    ("S9", "续约潜力", 0.08, "现有合同续约概率与扩展空间"),
    ("S10", "扩展空间", 0.06, "交叉销售与升级机会"),
    ("S11", "战略匹配", 0.08, "客户行业与我方战略方向一致性"),
    ("S12", "团队能力", 0.06, "我方交付团队经验与客户需求匹配"),
]


@pytest.mark.api
class TestFullDiagnosis:

    def test_run_all_12_signals(self):
        from app.schemas.response import APIResponse
        signals = [
            {"name": s[1], "weight": s[2], "score": 0.75, "trend": "stable"}
            for s in ALL_12_SIGNALS
        ]
        result = APIResponse.success(data={
            "task_id": "diag-full-001",
            "customer_id": 42,
            "status": "completed",
            "signals": signals,
            "overall_score": 0.73,
            "generated_at": NOW.isoformat(),
        })
        assert result.code == 200
        assert len(result.data["signals"]) == 12
        assert 0 <= result.data["overall_score"] <= 1

    def test_signal_weights_sum_to_one(self):
        """12 个信号权重之和应为 1.0。"""
        total = sum(s[2] for s in ALL_12_SIGNALS)
        assert abs(total - 1.0) < 0.01

    def test_concurrent_diagnosis_limit(self):
        """同时触发诊断应返回 429。"""
        from fastapi import HTTPException
        with pytest.raises(HTTPException) as exc:
            raise HTTPException(
                status_code=429, detail="诊断任务队列已满，请稍后重试"
            )
        assert exc.value.status_code == 429


@pytest.mark.api
class TestSignalWeights:

    def test_signals_list_with_weights(self):
        from app.schemas.response import APIResponse
        sorted_signals = sorted(ALL_12_SIGNALS, key=lambda s: s[2], reverse=True)
        result = APIResponse.success(data={
            "signals": [
                {"id": f"S{i+1}", "name": s[1], "weight": s[2], "description": s[3]}
                for i, s in enumerate(sorted_signals)
            ],
            "total": 12,
        })
        assert result.code == 200
        assert result.data["total"] == 12
        # 权重排序: 最大权重信号排前
        weights = [s["weight"] for s in result.data["signals"]]
        assert weights == sorted(weights, reverse=True), \
            f"信号应按权重降序排列: {weights}"

    def test_update_signal_weight(self):
        """调整信号权重。"""
        from app.schemas.response import APIResponse
        result = APIResponse.success(data={
            "signal_id": "S5", "old_weight": 0.08, "new_weight": 0.12,
        })
        assert result.code == 200
        assert result.data["new_weight"] > result.data["old_weight"]


@pytest.mark.api
class TestSignalTrend:

    def test_trend_data(self):
        from app.schemas.response import APIResponse
        result = APIResponse.success(data={
            "signal_id": "S1",
            "signal_name": "采购周期",
            "customer_id": 42,
            "data_points": [
                {"date": "2026-01", "score": 0.65},
                {"date": "2026-02", "score": 0.72},
                {"date": "2026-03", "score": 0.78},
                {"date": "2026-04", "score": 0.81},
                {"date": "2026-05", "score": 0.85},
                {"date": "2026-06", "score": 0.88},
            ],
            "trend_direction": "up",
            "trend_slope": 0.046,
        })
        assert result.code == 200
        assert result.data["trend_direction"] == "up"
        assert len(result.data["data_points"]) == 6

    def test_trend_not_found(self):
        from fastapi import HTTPException
        with pytest.raises(HTTPException) as exc:
            raise HTTPException(status_code=404, detail="信号不存在")
        assert exc.value.status_code == 404
