from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from datetime import datetime, timezone
from app.core.database import get_db
from app.models.relationship import Relationship
from app.schemas.relationship import RelationshipCreate, RelationshipUpdate, RelationshipResponse
from app.schemas.response import APIResponse, PaginatedData

router = APIRouter()

@router.post("/", response_model=APIResponse[RelationshipResponse])
def create_relationship(body: RelationshipCreate, db: Session = Depends(get_db)):
    r = Relationship(**body.model_dump())
    db.add(r)
    db.commit()
    db.refresh(r)
    return APIResponse.success(data=RelationshipResponse.model_validate(r))

@router.get("/customer/{customer_id}", response_model=APIResponse[list[RelationshipResponse]])
def list_by_customer(customer_id: int, db: Session = Depends(get_db)):
    items = db.query(Relationship).filter(Relationship.customer_id == customer_id).order_by(Relationship.created_at.desc()).all()
    return APIResponse.success(data=[RelationshipResponse.model_validate(i) for i in items])

@router.put("/{r_id}", response_model=APIResponse[RelationshipResponse])
def update_relationship(r_id: int, body: RelationshipUpdate, db: Session = Depends(get_db)):
    r = db.query(Relationship).filter(Relationship.id == r_id).first()
    if not r:
        raise HTTPException(status_code=404, detail="记录不存在")
    for k, v in body.model_dump(exclude_unset=True).items():
        setattr(r, k, v)
    r.updated_at = datetime.now(timezone.utc)
    db.commit()
    db.refresh(r)
    return APIResponse.success(data=RelationshipResponse.model_validate(r))

@router.delete("/{r_id}", response_model=APIResponse[None])
def delete_relationship(r_id: int, db: Session = Depends(get_db)):
    r = db.query(Relationship).filter(Relationship.id == r_id).first()
    if not r:
        raise HTTPException(status_code=404)
    db.delete(r)
    db.commit()
    return APIResponse.success(message="删除成功")
