<<<<<<< HEAD
from __future__ import annotations

from datetime import datetime, timezone
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Query, status
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.security import get_current_user, CurrentUser
from app.schemas.response import APIResponse, PaginatedData
from app.services.vector_service import VectorService

router = APIRouter()

# File upload safety limits
MAX_FILE_SIZE = 10 * 1024 * 1024  # 10 MB
ALLOWED_EXTENSIONS = {".pdf", ".docx", ".txt", ".md", ".csv", ".json", ".html"}
ALLOWED_MIME_TYPES = {
    "application/pdf",
    "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
    "text/plain",
    "text/markdown",
    "text/csv",
    "application/json",
    "text/html",
}


class KnowledgeDocCreate(BaseModel):
    title: str = Field(..., min_length=1, max_length=200)
    content: str = Field(..., min_length=1, max_length=100_000)
    collection: str = Field(default="default", max_length=50)


class KnowledgeDocResponse(BaseModel):
    id: int
    title: str
    collection: str
    created_at: datetime
    updated_at: datetime
    model_config = {"from_attributes": True}


@router.post("/", response_model=APIResponse[KnowledgeDocResponse])
def create_doc(
    body: KnowledgeDocCreate,
    db: Session = Depends(get_db),
    user: CurrentUser = Depends(get_current_user),
):
    """Upload a knowledge document. Content is indexed into the vector store."""
    # Placeholder: store document in DB + index in vector service
    vector_svc = VectorService(db)
    vector_svc.index_document(
        document_id=0,  # placeholder
        content=body.content,
        tenant_id=user.id,
        metadata={"title": body.title, "collection": body.collection},
    )
    # Return placeholder response
    return APIResponse.success(data=KnowledgeDocResponse(
        id=1, title=body.title, collection=body.collection,
        created_at=datetime.now(timezone.utc),
        updated_at=datetime.now(timezone.utc),
    ))


@router.get("/", response_model=APIResponse[PaginatedData[KnowledgeDocResponse]])
def list_docs(
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=20, ge=1, le=100),
    collection: Optional[str] = None,
    search: Optional[str] = None,
    db: Session = Depends(get_db),
    user: CurrentUser = Depends(get_current_user),
):
    """List knowledge documents. Tenant-scoped."""
    # Placeholder
    return APIResponse.success(data=PaginatedData(
        items=[], total=0, page=page, page_size=page_size, total_pages=0,
    ))


@router.get("/{doc_id}", response_model=APIResponse[KnowledgeDocResponse])
def get_doc(
    doc_id: int,
    db: Session = Depends(get_db),
    user: CurrentUser = Depends(get_current_user),
):
    """Get a knowledge document by ID."""
    raise HTTPException(status_code=404, detail="文档不存在")


@router.delete("/{doc_id}", response_model=APIResponse)
def delete_doc(
    doc_id: int,
    db: Session = Depends(get_db),
    user: CurrentUser = Depends(get_current_user),
):
    """Delete a knowledge document and its vectors."""
    vector_svc = VectorService(db)
    ok = vector_svc.delete_document(doc_id, tenant_id=user.id)
    if not ok:
        raise HTTPException(status_code=404, detail="文档不存在")
    return APIResponse.success(message="删除成功")


@router.post("/search", response_model=APIResponse[list[dict]])
def search_knowledge(
    query: str = Query(..., min_length=1, max_length=2000),
    top_k: int = Query(default=5, ge=1, le=20),
    collection: str = Query(default="default", max_length=50),
    db: Session = Depends(get_db),
    user: CurrentUser = Depends(get_current_user),
):
    """Semantic search over the knowledge base. Tenant-scoped."""
    vector_svc = VectorService(db)
    results = vector_svc.search(
        query=query,
        tenant_id=user.id,
        collection=collection,
        top_k=top_k,
    )
    return APIResponse.success(data=results)
=======
from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.knowledge import Knowledge
from app.services.vector_service import index_document, search_similar
from app.schemas.response import APIResponse
from pydantic import BaseModel, Field

router = APIRouter()


class SearchRequest(BaseModel):
    q: str = Field(..., min_length=1)
    category: Optional[str] = None
    top_k: int = Field(default=5, ge=1, le=20)


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


@router.post("/search", response_model=APIResponse[list])
def semantic_search(body: SearchRequest, db: Session = Depends(get_db)):
    results = search_similar(db, body.q, body.top_k, body.category)
    return APIResponse.success(data=results)


@router.post("/documents", response_model=APIResponse[dict])
def upload_document(body: KnowledgeCreate, db: Session = Depends(get_db)):
    k = Knowledge(**body.model_dump())
    db.add(k)
    db.commit()
    db.refresh(k)
    index_document(db, k.id)
    return APIResponse.success(data={"id": k.id, "title": k.title, "message": "文档已向量化"})


@router.post("/", response_model=APIResponse[dict])
def create_knowledge(body: KnowledgeCreate, db: Session = Depends(get_db)):
    k = Knowledge(**body.model_dump())
    db.add(k)
    db.commit()
    db.refresh(k)
    return APIResponse.success(data={"id": k.id, "title": k.title, "category": k.category})


@router.get("/", response_model=APIResponse[dict])
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
    items = q.offset((page - 1) * page_size).limit(page_size).all()
    return APIResponse.success(data={"items": [{"id": k.id, "title": k.title, "category": k.category, "tags": k.tags, "created_at": k.created_at.isoformat()} for k in items], "total": total, "page": page, "page_size": page_size})


@router.get("/{k_id}", response_model=APIResponse[dict])
def get_knowledge(k_id: int, db: Session = Depends(get_db)):
    k = db.query(Knowledge).filter(Knowledge.id == k_id).first()
    if not k:
        raise HTTPException(404, "知识条目不存在")
    return APIResponse.success(data={"id": k.id, "title": k.title, "content": k.content, "category": k.category, "tags": k.tags, "source": k.source})


@router.put("/{k_id}/reindex", response_model=APIResponse[dict])
def reindex_document(k_id: int, db: Session = Depends(get_db)):
    k = db.query(Knowledge).filter(Knowledge.id == k_id).first()
    if not k:
        raise HTTPException(404)
    index_document(db, k_id)
    return APIResponse.success(data={"id": k_id, "message": "重新向量化完成"})


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
>>>>>>> 662f12488696422c660a7b9ff57a0f880cf8e5a8
