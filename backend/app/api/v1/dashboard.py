from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func
from datetime import datetime, timezone, timedelta
from app.core.database import get_db
from app.core.security import get_current_user, CurrentUser
from app.models.bidding import Bidding
from app.models.project import Project
from app.models.organization import Organization
from app.models.crm_relationship import CrmRelationship
from app.models.action_item import ActionItem
from app.models.ai_work_summary import AiWorkSummary
from app.schemas.response import APIResponse

router = APIRouter()


@router.get("/stats", response_model=APIResponse[dict])
def dashboard_stats(db: Session = Depends(get_db), user: CurrentUser = Depends(get_current_user)):
    now = datetime.now(timezone.utc)
    month_start = now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)

    total_customers = db.query(func.count(Organization.id)).filter(
        Organization.deleted_at.is_(None), Organization.org_type == "company"
    ).scalar() or 0

    total_projects = db.query(func.count(Project.id)).filter(
        Project.deleted_at.is_(None)
    ).scalar() or 0

    active_bids = db.query(func.count(Bidding.id)).filter(
        Bidding.deleted_at.is_(None), Bidding.bid_status.in_([1, 2, 3, 4])
    ).scalar() or 0

    won_bids = db.query(func.count(Bidding.id)).filter(
        Bidding.deleted_at.is_(None), Bidding.bid_status == 5
    ).scalar() or 0

    month_visits = db.query(func.count(CrmRelationship.id)).filter(
        CrmRelationship.visit_date >= month_start
    ).scalar() or 0

    pending_actions = db.query(func.count(ActionItem.id)).filter(
        ActionItem.is_done == False
    ).scalar() or 0

    overdue_actions = db.query(func.count(ActionItem.id)).filter(
        ActionItem.is_done == False,
        ActionItem.due_date < now,
    ).scalar() or 0

    project_stages = db.query(Project.stage, func.count(Project.id)).filter(
        Project.deleted_at.is_(None)
    ).group_by(Project.stage).all()

    monthly_new = db.query(func.count(Project.id)).filter(
        Project.created_at >= month_start, Project.deleted_at.is_(None)
    ).scalar() or 0

    monthly_reports = db.query(func.count(AiWorkSummary.id)).filter(
        AiWorkSummary.created_at >= month_start
    ).scalar() or 0

    return APIResponse.success(data={
        "customers": {"total": total_customers},
        "projects": {"total": total_projects, "new_this_month": monthly_new},
        "bidding": {"active": active_bids, "won": won_bids},
        "visits": {"this_month": month_visits},
        "actions": {"pending": pending_actions, "overdue": overdue_actions},
        "reports": {"this_month": monthly_reports},
        "pipeline": [{"stage": s, "stage_name": {1: "线索", 2: "商机", 3: "需求", 4: "方案", 5: "报价", 6: "谈判", 7: "合同", 8: "交付", 9: "验收", 10: "回款", 11: "运维", 12: "结项"}.get(s, str(s)), "count": c} for s, c in project_stages],
    })
