from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import desc, asc
from app.core.database import get_db
from app.models.customer import Customer
from app.schemas.customer import CustomerCreate, CustomerUpdate, CustomerResponse
from app.schemas.response import APIResponse, PaginatedData

router = APIRouter()


@router.post("/", response_model=APIResponse[CustomerResponse])
def create(body: CustomerCreate, db: Session = Depends(get_db)):
    if body.code and db.query(Customer).filter(Customer.code == body.code).first():
        raise HTTPException(400, "客户编码已存在")
    c = Customer(**body.model_dump())
    db.add(c); db.commit(); db.refresh(c)
    return APIResponse.success(data=CustomerResponse.model_validate(c))


@router.get("/", response_model=APIResponse[PaginatedData[CustomerResponse]])
def list_customers(
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=20, ge=1, le=100),
    sort_order: str = Query(default="desc", pattern="^(asc|desc)$"),
    search: Optional[str] = None,
    industry: Optional[str] = None,
    level: Optional[str] = None,
    source: Optional[str] = None,
    is_active: Optional[bool] = None,
    db: Session = Depends(get_db),
):
    q = db.query(Customer)
    if search:
        q = q.filter(Customer.name.ilike(f"%{search}%") | Customer.code.ilike(f"%{search}%"))
    if industry:
        q = q.filter(Customer.industry == industry)
    if level:
        q = q.filter(Customer.level == level)
    if source:
        q = q.filter(Customer.source == source)
    if is_active is not None:
        q = q.filter(Customer.is_active == is_active)
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
def get(customer_id: int, db: Session = Depends(get_db)):
    c = db.query(Customer).filter(Customer.id == customer_id).first()
    if not c:
        raise HTTPException(404, "客户不存在")
    return APIResponse.success(data=CustomerResponse.model_validate(c))


@router.put("/{customer_id}", response_model=APIResponse[CustomerResponse])
def update(customer_id: int, body: CustomerUpdate, db: Session = Depends(get_db)):
    c = db.query(Customer).filter(Customer.id == customer_id).first()
    if not c:
        raise HTTPException(404)
    for k, v in body.model_dump(exclude_unset=True).items():
        setattr(c, k, v)
    db.commit(); db.refresh(c)
    return APIResponse.success(data=CustomerResponse.model_validate(c))


@router.delete("/{customer_id}", response_model=APIResponse[None])
def delete(customer_id: int, db: Session = Depends(get_db)):
    c = db.query(Customer).filter(Customer.id == customer_id).first()
    if not c:
        raise HTTPException(404)
    c.is_active = False; db.commit()
    return APIResponse.success(message="已禁用")


@router.get("/export/all", response_model=APIResponse[list[CustomerResponse]])
def export_all(db: Session = Depends(get_db)):
    items = db.query(Customer).filter(Customer.is_active == True).order_by(Customer.created_at.desc()).all()
    return APIResponse.success(data=[CustomerResponse.model_validate(i) for i in items])
