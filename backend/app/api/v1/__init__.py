from fastapi import APIRouter
from app.api.v1 import bidding, projects, organizations, ai_diagnosis

router = APIRouter()
router.include_router(bidding.router, prefix="/bidding", tags=["招投标管理"])
router.include_router(projects.router, prefix="/projects", tags=["项目管理"])
router.include_router(organizations.router, prefix="/organizations", tags=["组织层级"])
router.include_router(ai_diagnosis.router, prefix="/ai", tags=["AI智能模块"])
