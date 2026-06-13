from fastapi import APIRouter
from app.api.v1.ai import reports

router = APIRouter()
router.include_router(reports.router, prefix="/ai/reports", tags=["AI报告"])
