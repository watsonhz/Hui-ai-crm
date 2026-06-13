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
