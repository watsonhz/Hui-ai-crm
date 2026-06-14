from fastapi import APIRouter, Depends
from pydantic import BaseModel, Field
from typing import Optional
from app.schemas.response import APIResponse
from app.core.security import get_current_user, CurrentUser

router = APIRouter()


class LeadScoreRequest(BaseModel):
    company_name: str
    industry: str
    company_size: int = Field(default=0, ge=0)
    annual_revenue: Optional[float] = None
    existing_relationship: bool = False


class ChurnRequest(BaseModel):
    customer_id: int
    recent_activity_days: int = 30
    support_tickets: int = 0
    contract_expiry_days: Optional[int] = None


class ForecastRequest(BaseModel):
    quarter: str = Field(default="Q3", pattern="^Q[1-4]$")
    year: int = Field(default=2026, ge=2024, le=2030)


@router.post("/lead-scoring", response_model=APIResponse[dict])
def lead_scoring(body: LeadScoreRequest, user: CurrentUser = Depends(get_current_user)):
    score = 50
    if body.existing_relationship:
        score += 20
    if body.annual_revenue and body.annual_revenue > 1_000_000:
        score += 15
    if body.company_size > 100:
        score += 10
    level = "hot" if score >= 75 else "warm" if score >= 50 else "cold"
    return APIResponse.success(data={"company": body.company_name, "score": score, "level": level,
        "factors": {"relationship": body.existing_relationship, "revenue": body.annual_revenue, "size": body.company_size}})


@router.post("/churn-prediction", response_model=APIResponse[dict])
def churn_prediction(body: ChurnRequest, user: CurrentUser = Depends(get_current_user)):
    risk = 0
    factors = []
    if body.recent_activity_days > 90:
        risk += 30; factors.append("长期未活跃")
    if body.support_tickets > 5:
        risk += 25; factors.append("工单过多")
    if body.contract_expiry_days and body.contract_expiry_days < 30:
        risk += 25; factors.append("合同即将到期")
    if body.contract_expiry_days and body.contract_expiry_days < 0:
        risk += 20; factors.append("合同已过期")
    level = "high" if risk >= 50 else "medium" if risk >= 25 else "low"
    return APIResponse.success(data={"customer_id": body.customer_id, "churn_risk": risk, "level": level, "factors": factors})


@router.get("/upsell-opportunities/{customer_id}", response_model=APIResponse[list])
def upsell_opportunities(customer_id: int):
    return APIResponse.success(data=[
        {"product": "高级数据分析模块", "estimated_value": 50000, "confidence": "high"},
        {"product": "AI智能客服升级", "estimated_value": 30000, "confidence": "medium"},
        {"product": "移动端App套装", "estimated_value": 20000, "confidence": "low"},
    ])


@router.get("/sales-forecast", response_model=APIResponse[dict])
def sales_forecast(quarter: str = "Q3", year: int = 2026):
    return APIResponse.success(data={
        "quarter": f"{year} {quarter}",
        "predicted_revenue": 2500000,
        "pipeline_value": 5800000,
        "win_rate": 0.35,
        "top_deals": [
            {"name": "智慧城市二期", "amount": 800000, "probability": 0.6},
            {"name": "银行数据平台", "amount": 500000, "probability": 0.4},
        ],
    })
