from fastapi import APIRouter
from app.api.v1 import (
    bidding, projects, organizations, ai_diagnosis, decision_chain,
    acceptance, relationships, auth, system, ai_service, knowledge,
)

router = APIRouter()
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
