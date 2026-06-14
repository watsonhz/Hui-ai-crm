from fastapi import APIRouter, Depends
from pydantic import BaseModel, Field
from typing import Optional
from app.schemas.response import APIResponse
<<<<<<< HEAD
=======
from app.core.security import get_current_user, CurrentUser
>>>>>>> 662f12488696422c660a7b9ff57a0f880cf8e5a8

router = APIRouter()


class CampaignRequest(BaseModel):
    target_segment: str = Field(..., min_length=1)
    budget: float = Field(default=0, ge=0)
    goal: str = "lead_generation"


class ContentRequest(BaseModel):
    topic: str = Field(..., min_length=1)
    content_type: str = Field(default="email", pattern="^(email|social|blog|ad)$")
    target_audience: str = "企业决策者"
    tone: str = Field(default="professional", pattern="^(professional|casual|technical)$")


class RoiRequest(BaseModel):
    campaign_ids: list[int] = []
    start_date: Optional[str] = None
    end_date: Optional[str] = None


@router.post("/campaign-recommend", response_model=APIResponse[dict])
<<<<<<< HEAD
def campaign_recommend(body: CampaignRequest):
=======
def campaign_recommend(body: CampaignRequest, user: CurrentUser = Depends(get_current_user)):
>>>>>>> 662f12488696422c660a7b9ff57a0f880cf8e5a8
    campaigns = []
    if body.budget >= 100000:
        campaigns.append({"name": "行业峰会赞助", "estimated_reach": 5000, "estimated_leads": 200, "cost": 80000})
    if body.budget >= 50000:
        campaigns.append({"name": "线上研讨会系列", "estimated_reach": 3000, "estimated_leads": 150, "cost": 40000})
    campaigns.append({"name": "精准邮件营销", "estimated_reach": 2000, "estimated_leads": 100, "cost": 15000})
    return APIResponse.success(data={"segment": body.target_segment, "recommended_campaigns": campaigns,
        "total_estimated_leads": sum(c["estimated_leads"] for c in campaigns)})


@router.post("/content-generate", response_model=APIResponse[dict])
<<<<<<< HEAD
def content_generate(body: ContentRequest):
=======
def content_generate(body: ContentRequest, user: CurrentUser = Depends(get_current_user)):
>>>>>>> 662f12488696422c660a7b9ff57a0f880cf8e5a8
    templates = {
        "email": f"主题: 助力{body.target_audience}数字化转型\n\n尊敬的{body.target_audience}：\n\n我们诚邀您了解最新的{body.topic}解决方案...",
        "social": f"🚀 {body.topic}新突破！为{body.target_audience}量身打造...",
        "blog": f"# {body.topic}深度解析\n\n在当今数字化浪潮中，{body.target_audience}面临着前所未有的挑战与机遇...",
        "ad": f"【精准触达】{body.topic} — 专为{body.target_audience}设计，立即了解>>",
    }
    return APIResponse.success(data={"content_type": body.content_type, "tone": body.tone,
        "content": templates.get(body.content_type, templates["email"])})


@router.get("/roi-analysis", response_model=APIResponse[dict])
def roi_analysis(start_date: str = None, end_date: str = None):
    return APIResponse.success(data={
        "period": f"{start_date or '年初'} 至 {end_date or '至今'}",
        "total_spend": 250000,
        "total_leads": 850,
        "total_conversions": 45,
        "revenue_generated": 1800000,
        "roi_percent": 620,
        "channels": [
            {"channel": "邮件营销", "spend": 50000, "leads": 300, "conversions": 18, "roi": 720},
            {"channel": "社交媒体", "spend": 80000, "leads": 250, "conversions": 12, "roi": 450},
            {"channel": "行业活动", "spend": 120000, "leads": 300, "conversions": 15, "roi": 500},
        ],
    })
