from __future__ import annotations

from datetime import datetime, timezone
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
from sqlalchemy import desc, asc

from app.core.database import get_db
from app.core.security import get_current_user, CurrentUser
from app.models.customer import Customer
from app.schemas.customer import CustomerCreate, CustomerUpdate, CustomerResponse
from app.schemas.response import APIResponse, PaginatedData

router = APIRouter()


def _escape_like(value: str) -> str:
    return value.replace("\\", "\\\\").replace("%", "\\%").replace("_", "\\_")


@router.post("/", response_model=APIResponse[CustomerResponse])
def create(body: CustomerCreate, db: Session = Depends(get_db), user: CurrentUser = Depends(get_current_user)):
    data = body.model_dump()
    data["owner_id"] = user.id
    customer = Customer(**data)
    db.add(customer)
    db.commit()
    db.refresh(customer)
    return APIResponse.success(data=CustomerResponse.model_validate(customer))


@router.get("/", response_model=APIResponse[PaginatedData[CustomerResponse]])
def list(
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=20, ge=1, le=100),
    sort_order: str = Query(default="desc", pattern="^(asc|desc)$"),
    name: Optional[str] = None,
    company: Optional[str] = None,
    status: Optional[str] = None,
    level: Optional[str] = None,
    source: Optional[str] = None,
    db: Session = Depends(get_db),
    user: CurrentUser = Depends(get_current_user),
):
    q = db.query(Customer).filter(Customer.deleted_at.is_(None))
    if name:
        q = q.filter(Customer.name.ilike(f"%{_escape_like(name)}%"))
    if company:
        q = q.filter(Customer.company.ilike(f"%{_escape_like(company)}%"))
    if status:
        q = q.filter(Customer.status == status)
    if level:
        q = q.filter(Customer.level == level)
    if source:
        q = q.filter(Customer.source == source)
    order_fn = desc if sort_order == "desc" else asc
    q = q.order_by(order_fn(Customer.created_at))
    total = q.count()
    items = q.offset((page - 1) * page_size).limit(page_size).all()
    return APIResponse.success(data=PaginatedData(
        items=[CustomerResponse.model_validate(i) for i in items],
        total=total, page=page, page_size=page_size,
        total_pages=(total + page_size - 1) // page_size,
    ))


@router.get("/{customer_id}", response_model=APIResponse[CustomerResponse])
def get(customer_id: int, db: Session = Depends(get_db), user: CurrentUser = Depends(get_current_user)):
    customer = db.query(Customer).filter(
        Customer.id == customer_id, Customer.deleted_at.is_(None)
    ).first()
    if not customer:
        raise HTTPException(status_code=404, detail="客户不存在")
    return APIResponse.success(data=CustomerResponse.model_validate(customer))


@router.put("/{customer_id}", response_model=APIResponse[CustomerResponse])
def update(customer_id: int, body: CustomerUpdate, db: Session = Depends(get_db), user: CurrentUser = Depends(get_current_user)):
    customer = db.query(Customer).filter(
        Customer.id == customer_id, Customer.deleted_at.is_(None)
    ).first()
    if not customer:
        raise HTTPException(status_code=404, detail="客户不存在")
    if customer.owner_id != user.id and user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="无权修改此客户",
        )
    for k, v in body.model_dump(exclude_unset=True).items():
        setattr(customer, k, v)
    customer.updated_at = datetime.now(timezone.utc)
    db.commit()
    db.refresh(customer)
    return APIResponse.success(data=CustomerResponse.model_validate(customer))


@router.delete("/{customer_id}", response_model=APIResponse)
def delete(customer_id: int, db: Session = Depends(get_db), user: CurrentUser = Depends(get_current_user)):
    customer = db.query(Customer).filter(
        Customer.id == customer_id, Customer.deleted_at.is_(None)
    ).first()
    if not customer:
        raise HTTPException(status_code=404, detail="客户不存在")
    if customer.owner_id != user.id and user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="无权删除此客户",
        )
    customer.deleted_at = datetime.now(timezone.utc)
    db.commit()
    return APIResponse.success(message="删除成功")
