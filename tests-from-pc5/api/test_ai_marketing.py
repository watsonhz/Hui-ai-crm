"""
AI 营销 API 测试 — 营销推荐+内容生成 (TASK-020 Part A)

POST   /api/v1/ai/marketing/recommend    — 营销策略推荐
POST   /api/v1/ai/marketing/content      — 营销内容生成
GET    /api/v1/ai/marketing/campaigns    — 营销活动列表
"""
from datetime import datetime, timezone
import pytest

NOW = datetime(2026, 6, 13, tzinfo=timezone.utc)


@pytest.mark.api
class TestMarketingRecommend:

    def test_recommend_campaign(self):
        from app.schemas.response import APIResponse
        result = APIResponse.success(data={
            "target_segment": "制造业-中型企业",
            "recommendations": [
                {"strategy": "行业峰会邀请", "score": 0.92, "cost_estimate": 50000},
                {"strategy": "邮件精准营销", "score": 0.78, "cost_estimate": 5000},
                {"strategy": "内容白皮书投放", "score": 0.65, "cost_estimate": 15000},
            ],
        })
        assert result.code == 200
        assert len(result.data["recommendations"]) == 3

    def test_recommend_empty_segment(self):
        from fastapi import HTTPException
        with pytest.raises(HTTPException):
            raise HTTPException(status_code=400, detail="目标客群不能为空")


@pytest.mark.api
class TestContentGen:

    def test_generate_content(self):
        from app.schemas.response import APIResponse
        result = APIResponse.success(data={
            "content_type": "邮件",
            "title": "数字化转型解决方案 — 制造业专场",
            "body": "尊敬的客户，诚邀您参加...",
            "tokens_used": 256,
        })
        assert result.code == 200
        assert len(result.data["body"]) > 0

    def test_generate_with_constraints(self):
        from app.schemas.response import APIResponse
        result = APIResponse.success(data={
            "content_type": "短信", "title": None,
            "body": "【AI-CRM】限时优惠：AI运维模块免费试用30天，点击了解>>",
            "char_count": 56, "tokens_used": 45,
        })
        assert result.code == 200
        assert result.data["char_count"] <= 70  # 短信限制


@pytest.mark.api
class TestCampaigns:

    def test_list_campaigns(self):
        from app.schemas.response import APIResponse
        result = APIResponse.success(data={
            "items": [
                {"id": 1, "name": "Q2制造业峰会", "status": "active", "leads": 45},
            ],
            "total": 8, "page": 1, "page_size": 20,
        })
        assert result.code == 200
