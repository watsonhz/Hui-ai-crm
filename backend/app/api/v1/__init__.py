from fastapi import APIRouter
from app.api.v1 import bidding, projects, organizations, auth

router = APIRouter()
router.include_router(auth.router, prefix="/auth", tags=["认证"])
router.include_router(bidding.router, prefix="/bidding", tags=["招投标管理"])
router.include_router(projects.router, prefix="/projects", tags=["项目管理"])
router.include_router(organizations.router, prefix="/organizations", tags=["组织层级"])
