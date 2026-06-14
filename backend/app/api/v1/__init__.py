from fastapi import APIRouter
<<<<<<< HEAD
router = APIRouter()

from app.api.v1.bidding import router as br; router.include_router(br, prefix="/bidding", tags=["Bidding"])
from app.api.v1.projects import router as pr; router.include_router(pr, prefix="/projects", tags=["Projects"])
from app.api.v1.organizations import router as or_; router.include_router(or_, prefix="/organizations", tags=["Organizations"])
from app.api.v1.customers import router as cr; router.include_router(cr, prefix="/customers", tags=["Customers"])
from app.api.v1.auth import router as ar; router.include_router(ar, prefix="/auth", tags=["Auth"])
from app.api.v1.ai_diagnosis import router as dr; router.include_router(dr, prefix="/ai/diagnosis", tags=["AI Diagnosis"])
from app.api.v1.ai_sales import router as asr; router.include_router(asr, prefix="/ai/sales", tags=["AI Sales"])
from app.api.v1.ai_marketing import router as amr; router.include_router(amr, prefix="/ai/marketing", tags=["AI Marketing"])
from app.api.v1.ai_service import router as avr; router.include_router(avr, prefix="/ai/service", tags=["AI Service"])
from app.api.v1.decision_chain import router as dcr; router.include_router(dcr, prefix="/decision-chain", tags=["Decision Chain"])
from app.api.v1.knowledge import router as kr; router.include_router(kr, prefix="/knowledge", tags=["Knowledge"])
from app.api.v1.service_tickets import router as str_; router.include_router(str_, prefix="/service/tickets", tags=["Tickets"])
from app.api.v1.system import router as sr; router.include_router(sr, prefix="/system", tags=["System"])
from app.api.v1.system_admin import router as sar; router.include_router(sar, prefix="/system/admin", tags=["Admin"])
from app.api.v1.workflow import router as wr; router.include_router(wr, prefix="/workflow", tags=["Workflow"])
=======
from app.api.v1 import (
    bidding, projects, organizations, ai_diagnosis, decision_chain,
    acceptance, relationships, auth, system, ai_service, knowledge, dashboard, service_tickets, workflow,
    ai_sales, ai_marketing, system_admin, customers,
)

router = APIRouter()

# Core modules (always load)
from app.api.v1 import auth, bidding, projects, organizations
router.include_router(auth.router, prefix="/auth", tags=["认证授权"])
router.include_router(bidding.router, prefix="/bidding", tags=["招投标管理"])
router.include_router(projects.router, prefix="/projects", tags=["项目管理"])
router.include_router(organizations.router, prefix="/organizations", tags=["组织层级"])
router.include_router(ai_diagnosis.router, prefix="/ai", tags=["AI诊断报告"])
router.include_router(ai_service.router, prefix="/ai", tags=["AI智能服务"])
router.include_router(decision_chain.router, prefix="/decision-chain", tags=["决策链图谱"])
router.include_router(acceptance.router, prefix="/acceptance", tags=["验收管理"])
router.include_router(relationships.router, prefix="/relationships", tags=["关系维护"])
router.include_router(auth.router, prefix="/auth", tags=["认证授权"])
router.include_router(system.router, prefix="/system", tags=["系统管理"])
router.include_router(knowledge.router, prefix="/knowledge", tags=["RAG知识库"])
router.include_router(dashboard.router, prefix="/dashboard", tags=["数据看板"])
router.include_router(service_tickets.router, prefix="/ai/service/tickets", tags=["AI工单管理"])
router.include_router(workflow.router, prefix="/workflow", tags=["BPM工作流"])
router.include_router(ai_sales.router, prefix="/ai/sales", tags=["AI销售支持"])
router.include_router(ai_marketing.router, prefix="/ai/marketing", tags=["AI营销推广"])
router.include_router(system_admin.router, prefix="/system", tags=["系统管理(RBAC)"])
router.include_router(customers.router, prefix="/customers", tags=["客户管理"])
>>>>>>> 662f12488696422c660a7b9ff57a0f880cf8e5a8
