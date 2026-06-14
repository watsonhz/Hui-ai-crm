from fastapi import APIRouter, Depends
from pydantic import BaseModel, Field
from app.schemas.response import APIResponse
<<<<<<< HEAD
=======
from app.core.security import get_current_user, CurrentUser
>>>>>>> 662f12488696422c660a7b9ff57a0f880cf8e5a8
import os

router = APIRouter()

class ServiceQuery(BaseModel):
    customer_id: int
    question: str = Field(..., min_length=1)

class SalesAdvice(BaseModel):
    project_id: int
    context: str = ""

class MarketingPlan(BaseModel):
    customer_segment: str
    goal: str = ""

class OpsInsight(BaseModel):
    period: str = "monthly"

@router.post("/service", response_model=APIResponse[dict])
<<<<<<< HEAD
def ai_service(body: ServiceQuery):
=======
def ai_service(body: ServiceQuery, user: CurrentUser = Depends(get_current_user)):
>>>>>>> 662f12488696422c660a7b9ff57a0f880cf8e5a8
    api_key = os.environ.get("DEEPSEEK_API_KEY", "")
    if not api_key or api_key.startswith("sk-your-"):
        return APIResponse.success(data={"advice": "AI客服助手待配置DeepSeek API Key", "question": body.question})
    return APIResponse.success(data={"advice": f"[AI] 针对客户{body.customer_id}的问题：{body.question[:50]}...的服务建议", "question": body.question})

@router.post("/sales", response_model=APIResponse[dict])
<<<<<<< HEAD
def ai_sales(body: SalesAdvice):
    return APIResponse.success(data={"advice": f"[AI] 项目{body.project_id}销售策略建议", "context": body.context})

@router.post("/marketing", response_model=APIResponse[dict])
def ai_marketing(body: MarketingPlan):
    return APIResponse.success(data={"plan": f"[AI] {body.customer_segment}细分市场-{body.goal}营销方案"})

@router.post("/operations", response_model=APIResponse[dict])
def ai_operations(body: OpsInsight):
=======
def ai_sales(body: SalesAdvice, user: CurrentUser = Depends(get_current_user)):
    return APIResponse.success(data={"advice": f"[AI] 项目{body.project_id}销售策略建议", "context": body.context})

@router.post("/marketing", response_model=APIResponse[dict])
def ai_marketing(body: MarketingPlan, user: CurrentUser = Depends(get_current_user)):
    return APIResponse.success(data={"plan": f"[AI] {body.customer_segment}细分市场-{body.goal}营销方案"})

@router.post("/operations", response_model=APIResponse[dict])
def ai_operations(body: OpsInsight, user: CurrentUser = Depends(get_current_user)):
>>>>>>> 662f12488696422c660a7b9ff57a0f880cf8e5a8
    return APIResponse.success(data={"insight": f"[AI] {body.period}运营数据洞察报告"})
