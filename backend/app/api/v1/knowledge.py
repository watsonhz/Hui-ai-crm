from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.knowledge import Knowledge
from app.schemas.response import APIResponse
from pydantic import BaseModel, Field

router = APIRouter()

class KnowledgeCreate(BaseModel):
    title: str = Field(..., max_length=200)
    content: str = Field(..., min_length=1)
    category: str = Field(..., max_length=50)
    tags: Optional[str] = Field(None, max_length=500)
    source: Optional[str] = Field(None, max_length=200)

class KnowledgeUpdate(BaseModel):
    title: Optional[str] = Field(None, max_length=200)
    content: Optional[str] = None
    category: Optional[str] = Field(None, max_length=50)
    tags: Optional[str] = Field(None, max_length=500)

@router.post("/", response_model=APIResponse[dict])
def create_knowledge(body: KnowledgeCreate, db: Session = Depends(get_db)):
    k = Knowledge(**body.model_dump())
    db.add(k)
    db.commit()
    db.refresh(k)
    return APIResponse.success(data={"id": k.id, "title": k.title, "category": k.category})

@router.get("/", response_model=APIResponse[list])
def list_knowledge(
    category: Optional[str] = None,
    search: Optional[str] = None,
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=20, ge=1, le=100),
    db: Session = Depends(get_db),
):
    q = db.query(Knowledge).order_by(Knowledge.created_at.desc())
    if category:
        q = q.filter(Knowledge.category == category)
    if search:
        q = q.filter(Knowledge.title.ilike(f"%{search}%"))
    total = q.count()
    items = q.offset((page-1)*page_size).limit(page_size).all()
    return APIResponse.success(data={"items": [{"id": k.id, "title": k.title, "category": k.category, "tags": k.tags, "created_at": k.created_at.isoformat()} for k in items], "total": total, "page": page, "page_size": page_size})

@router.get("/{k_id}", response_model=APIResponse[dict])
def get_knowledge(k_id: int, db: Session = Depends(get_db)):
    k = db.query(Knowledge).filter(Knowledge.id == k_id).first()
    if not k:
        raise HTTPException(404, "知识条目不存在")
    return APIResponse.success(data={"id": k.id, "title": k.title, "content": k.content, "category": k.category, "tags": k.tags, "source": k.source})

@router.put("/{k_id}", response_model=APIResponse[dict])
def update_knowledge(k_id: int, body: KnowledgeUpdate, db: Session = Depends(get_db)):
    k = db.query(Knowledge).filter(Knowledge.id == k_id).first()
    if not k:
        raise HTTPException(404)
    for key, val in body.model_dump(exclude_unset=True).items():
        setattr(k, key, val)
    db.commit()
    return APIResponse.success(data={"id": k.id, "title": k.title})

@router.delete("/{k_id}", response_model=APIResponse[None])
def delete_knowledge(k_id: int, db: Session = Depends(get_db)):
    k = db.query(Knowledge).filter(Knowledge.id == k_id).first()
    if not k:
        raise HTTPException(404)
    db.delete(k)
    db.commit()
    return APIResponse.success(message="删除成功")
