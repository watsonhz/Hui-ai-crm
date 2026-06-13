from fastapi import APIRouter
from app.api.v1 import bidding, projects, organizations, auth, customers, knowledge, workflows
from app.api.v1.ai import router as ai_router

router = APIRouter()
router.include_router(auth.router, prefix="/auth", tags=["认证"])
router.include_router(bidding.router, prefix="/bidding", tags=["招投标管理"])
router.include_router(customers.router, prefix="/customers", tags=["客户管理"])
router.include_router(projects.router, prefix="/projects", tags=["项目管理"])
router.include_router(organizations.router, prefix="/organizations", tags=["组织层级"])
router.include_router(knowledge.router, prefix="/knowledge", tags=["知识库"])
router.include_router(workflows.router, prefix="/workflows", tags=["BPM工作流"])
router.include_router(ai_router, prefix="", tags=["AI"])
