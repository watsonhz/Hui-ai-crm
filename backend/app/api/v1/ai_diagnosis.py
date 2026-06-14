from typing import Optional
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from pydantic import BaseModel, Field
from app.core.database import get_db
from app.core.security import get_current_user, CurrentUser
from app.schemas.response import APIResponse
from app.services.diagnosis_engine import run_full_diagnosis
from app.services.report_generator import daily_report, weekly_report, monthly_report, regenerate_report
from app.models.ai_work_summary import AiWorkSummary

router = APIRouter()


class DiagnosisRequest(BaseModel):
    customer_id: int
    project_id: Optional[int] = None
    contacts: list[dict] = []
    competitor_entries: list[dict] = []
    identified_roles: list[str] = []
    required_roles: dict = {}
    support_level: int = 0
    expected_support: dict = {}


class ReportRegenRequest(BaseModel):
    report_id: int


@router.post("/diagnosis", response_model=APIResponse[list[dict]])
def run_diagnosis(body: DiagnosisRequest, db: Session = Depends(get_db), user: CurrentUser = Depends(get_current_user)):
    results = run_full_diagnosis(
        db=db,
        customer_id=body.customer_id,
        project_id=body.project_id,
        contacts=body.contacts,
        competitor_entries=body.competitor_entries,
        identified_roles=body.identified_roles,
        required_roles=body.required_roles,
        support_level=body.support_level,
        expected_support=body.expected_support,
    )
    return APIResponse.success(data=results)


@router.post("/reports/daily", response_model=APIResponse[dict])
def generate_daily(db: Session = Depends(get_db), user: CurrentUser = Depends(get_current_user)):
    report = daily_report(db)
    return APIResponse.success(data={"id": report.id, "title": report.title, "content": report.content})


@router.post("/reports/weekly", response_model=APIResponse[dict])
def generate_weekly(db: Session = Depends(get_db), user: CurrentUser = Depends(get_current_user)):
    report = weekly_report(db)
    return APIResponse.success(data={"id": report.id, "title": report.title, "content": report.content})


@router.post("/reports/monthly", response_model=APIResponse[dict])
def generate_monthly(db: Session = Depends(get_db), user: CurrentUser = Depends(get_current_user)):
    report = monthly_report(db)
    return APIResponse.success(data={"id": report.id, "title": report.title, "content": report.content})


@router.get("/reports/{report_id}", response_model=APIResponse[dict])
def get_report(report_id: int, db: Session = Depends(get_db), user: CurrentUser = Depends(get_current_user)):
    report = db.query(AiWorkSummary).filter(AiWorkSummary.id == report_id).first()
    if not report:
        return APIResponse.error(message="报告不存在")
    return APIResponse.success(data={"id": report.id, "report_type": report.report_type, "title": report.title, "content": report.content, "period_start": report.period_start.isoformat() if report.period_start else None, "created_at": report.created_at.isoformat()})


@router.post("/reports/regenerate", response_model=APIResponse[dict])
def regenerate(body: ReportRegenRequest, db: Session = Depends(get_db), user: CurrentUser = Depends(get_current_user)):
    report = regenerate_report(db, body.report_id)
    if not report:
        return APIResponse.error(message="报告不存在")
    return APIResponse.success(data={"id": report.id, "title": report.title, "content": report.content})


@router.get("/reports", response_model=APIResponse[list[dict]])
def list_reports(
    report_type: Optional[str] = Query(None, pattern="^(daily|weekly|monthly)$"),
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=20, ge=1, le=100),
    db: Session = Depends(get_db),
):
    q = db.query(AiWorkSummary).order_by(AiWorkSummary.created_at.desc())
    if report_type:
        q = q.filter(AiWorkSummary.report_type == report_type)
    total = q.count()
    items = q.offset((page - 1) * page_size).limit(page_size).all()
    return APIResponse.success(data={
        "items": [{"id": r.id, "report_type": r.report_type, "title": r.title, "content": r.content, "created_at": r.created_at.isoformat()} for r in items],
        "total": total,
        "page": page,
        "page_size": page_size,
        "total_pages": (total + page_size - 1) // page_size,
    })
