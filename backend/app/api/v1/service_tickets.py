from datetime import datetime, timezone
from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from pydantic import BaseModel, Field
from app.core.database import get_db
<<<<<<< HEAD
=======
from app.core.security import get_current_user, CurrentUser
>>>>>>> 662f12488696422c660a7b9ff57a0f880cf8e5a8
from app.models.service_ticket import ServiceTicket
from app.services.sla_engine import calculate_sla, check_overdue
from app.schemas.response import APIResponse, PaginatedData

router = APIRouter()


class TicketCreate(BaseModel):
    title: str = Field(..., max_length=200)
    description: Optional[str] = None
    customer_id: int
    priority: int = Field(default=2, ge=0, le=3)
    customer_level: str = Field(default="normal", pattern="^(vip|key|normal)$")


class TicketUpdate(BaseModel):
    status: Optional[int] = Field(None, ge=1, le=4)
    assignee_id: Optional[int] = None
    resolution: Optional[str] = None
    priority: Optional[int] = Field(None, ge=0, le=3)


@router.post("/", response_model=APIResponse[dict])
<<<<<<< HEAD
def create_ticket(body: TicketCreate, db: Session = Depends(get_db)):
=======
def create_ticket(body: TicketCreate, db: Session = Depends(get_db), user: CurrentUser = Depends(get_current_user)):
>>>>>>> 662f12488696422c660a7b9ff57a0f880cf8e5a8
    sla = calculate_sla(body.customer_level)
    t = ServiceTicket(**body.model_dump(), **sla)
    db.add(t)
    db.commit()
    db.refresh(t)
    return APIResponse.success(data={"id": t.id, "title": t.title, "status": t.status,
        "sla_response_hours": t.sla_response_hours, "response_deadline": t.response_deadline.isoformat() if t.response_deadline else None})


@router.get("/", response_model=APIResponse[dict])
def list_tickets(
    status: Optional[int] = Query(None, ge=1, le=4),
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=20, ge=1, le=100),
    db: Session = Depends(get_db),
):
    q = db.query(ServiceTicket).order_by(ServiceTicket.created_at.desc())
    if status is not None:
        q = q.filter(ServiceTicket.status == status)
    total = q.count()
    items = q.offset((page - 1) * page_size).limit(page_size).all()
    return APIResponse.success(data={"items": [{"id": t.id, "title": t.title, "status": t.status, "priority": t.priority,
        "assignee_id": t.assignee_id, "is_overdue": check_overdue(t), "created_at": t.created_at.isoformat()} for t in items],
        "total": total, "page": page, "page_size": page_size})


@router.put("/{ticket_id}", response_model=APIResponse[dict])
<<<<<<< HEAD
def update_ticket(ticket_id: int, body: TicketUpdate, db: Session = Depends(get_db)):
=======
def update_ticket(ticket_id: int, body: TicketUpdate, db: Session = Depends(get_db), user: CurrentUser = Depends(get_current_user)):
>>>>>>> 662f12488696422c660a7b9ff57a0f880cf8e5a8
    t = db.query(ServiceTicket).filter(ServiceTicket.id == ticket_id).first()
    if not t:
        raise HTTPException(404, "工单不存在")
    for k, v in body.model_dump(exclude_unset=True).items():
        setattr(t, k, v)
    t.is_overdue = check_overdue(t)
    t.updated_at = datetime.now(timezone.utc)
    db.commit()
    return APIResponse.success(data={"id": t.id, "title": t.title, "status": t.status, "is_overdue": t.is_overdue})
