from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.decision_chain import DecisionChain
from app.schemas.decision_chain import DecisionChainCreate, DecisionChainUpdate, DecisionChainResponse
from app.schemas.response import APIResponse

router = APIRouter()

@router.post("/", response_model=APIResponse[DecisionChainResponse])
def create_decision_chain(body: DecisionChainCreate, db: Session = Depends(get_db)):
    dc = DecisionChain(**body.model_dump())
    db.add(dc)
    db.commit()
    db.refresh(dc)
    return APIResponse.success(data=DecisionChainResponse.model_validate(dc))

@router.get("/project/{project_id}", response_model=APIResponse[list[DecisionChainResponse]])
def list_by_project(project_id: int, db: Session = Depends(get_db)):
    items = db.query(DecisionChain).filter(DecisionChain.project_id == project_id).order_by(DecisionChain.weight.desc()).all()
    return APIResponse.success(data=[DecisionChainResponse.model_validate(i) for i in items])

@router.put("/{dc_id}", response_model=APIResponse[DecisionChainResponse])
def update_decision_chain(dc_id: int, body: DecisionChainUpdate, db: Session = Depends(get_db)):
    dc = db.query(DecisionChain).filter(DecisionChain.id == dc_id).first()
    if not dc:
        raise HTTPException(status_code=404, detail="记录不存在")
    for k, v in body.model_dump(exclude_unset=True).items():
        setattr(dc, k, v)
    dc.updated_at = __import__('datetime').datetime.now(__import__('datetime').timezone.utc)
    db.commit()
    db.refresh(dc)
    return APIResponse.success(data=DecisionChainResponse.model_validate(dc))

@router.delete("/{dc_id}", response_model=APIResponse[None])
def delete_decision_chain(dc_id: int, db: Session = Depends(get_db)):
    dc = db.query(DecisionChain).filter(DecisionChain.id == dc_id).first()
    if not dc:
        raise HTTPException(status_code=404)
    db.delete(dc)
    db.commit()
    return APIResponse.success(message="删除成功")
