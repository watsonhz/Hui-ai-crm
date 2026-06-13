from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from datetime import datetime, timezone
from app.core.database import get_db
from app.models.acceptance import Acceptance
from app.schemas.acceptance import AcceptanceCreate, AcceptanceUpdate, AcceptanceResponse
from app.schemas.response import APIResponse, PaginatedData

router = APIRouter()

@router.post("/", response_model=APIResponse[AcceptanceResponse])
def create_acceptance(body: AcceptanceCreate, db: Session = Depends(get_db)):
    a = Acceptance(**body.model_dump())
    db.add(a)
    db.commit()
    db.refresh(a)
    return APIResponse.success(data=AcceptanceResponse.model_validate(a))

@router.get("/project/{project_id}", response_model=APIResponse[list[AcceptanceResponse]])
def list_by_project(project_id: int, db: Session = Depends(get_db)):
    items = db.query(Acceptance).filter(Acceptance.project_id == project_id).order_by(Acceptance.created_at.desc()).all()
    return APIResponse.success(data=[AcceptanceResponse.model_validate(i) for i in items])

@router.put("/{a_id}", response_model=APIResponse[AcceptanceResponse])
def update_acceptance(a_id: int, body: AcceptanceUpdate, db: Session = Depends(get_db)):
    a = db.query(Acceptance).filter(Acceptance.id == a_id).first()
    if not a:
        raise HTTPException(status_code=404, detail="记录不存在")
    for k, v in body.model_dump(exclude_unset=True).items():
        setattr(a, k, v)
    a.updated_at = datetime.now(timezone.utc)
    db.commit()
    db.refresh(a)
    return APIResponse.success(data=AcceptanceResponse.model_validate(a))

@router.delete("/{a_id}", response_model=APIResponse[None])
def delete_acceptance(a_id: int, db: Session = Depends(get_db)):
    a = db.query(Acceptance).filter(Acceptance.id == a_id).first()
    if not a:
        raise HTTPException(status_code=404)
    db.delete(a)
    db.commit()
    return APIResponse.success(message="删除成功")
