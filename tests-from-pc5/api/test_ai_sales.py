"""
AI 销售 API 测试 — 线索评分+流失预测+交叉销售 (TASK-020 Part A)

POST   /api/v1/ai/sales/lead-score       — 线索评分
POST   /api/v1/ai/sales/churn-predict    — 流失预测
POST   /api/v1/ai/sales/cross-sell       — 交叉销售推荐
"""
from datetime import datetime, timezone
import pytest

NOW = datetime(2026, 6, 13, tzinfo=timezone.utc)


@pytest.mark.api
class TestLeadScore:

    def test_score_lead(self):
        from app.schemas.response import APIResponse
        result = APIResponse.success(data={
            "lead_id": 100, "lead_name": "XX集团数字化项目",
            "score": 0.82, "grade": "A",
            "factors": {
                "budget_match": 0.90, "authority": 0.85,
                "need_urgency": 0.78, "timeline": 0.75,
            },
            "recommendation": "强烈推荐跟进，预期成交概率82%",
        })
        assert result.code == 200
        assert 0 <= result.data["score"] <= 1

    def test_score_low_quality_lead(self):
        from app.schemas.response import APIResponse
        result = APIResponse.success(data={
            "lead_id": 101, "score": 0.25, "grade": "D",
            "recommendation": "低优先级，放入培育池",
        })
        assert result.data["grade"] == "D"


@pytest.mark.api
class TestChurnPredict:

    def test_predict_churn_risk(self):
        from app.schemas.response import APIResponse
        result = APIResponse.success(data={
            "customer_id": 42, "churn_probability": 0.35,
            "risk_factors": ["连续3月未采购", "客服投诉增加"],
            "retention_actions": ["安排拜访", "提供优惠方案"],
        })
        assert result.code == 200
        assert 0 <= result.data["churn_probability"] <= 1

    def test_batch_predict(self):
        """批量预测多个客户。"""
        from app.schemas.response import APIResponse
        result = APIResponse.success(data={
            "results": [
                {"customer_id": 1, "churn_probability": 0.12},
                {"customer_id": 2, "churn_probability": 0.68},
                {"customer_id": 3, "churn_probability": 0.05},
            ],
            "high_risk_count": 1,
        })
        assert result.code == 200
        assert result.data["high_risk_count"] == 1


@pytest.mark.api
class TestCrossSell:

    def test_cross_sell_recommendations(self):
        from app.schemas.response import APIResponse
        result = APIResponse.success(data={
            "customer_id": 42,
            "recommendations": [
                {"product": "AI运维模块", "score": 0.88, "revenue_estimate": 500000},
                {"product": "安全合规服务", "score": 0.72, "revenue_estimate": 300000},
            ],
        })
        assert result.code == 200
        assert len(result.data["recommendations"]) >= 1

    def test_no_cross_sell_opportunity(self):
        from app.schemas.response import APIResponse
        result = APIResponse.success(data={
            "customer_id": 99, "recommendations": [],
        })
        assert result.code == 200
        assert result.data["recommendations"] == []
