from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session
from typing import Optional

from app.core.database import get_db
from app.core.security import get_current_user, CurrentUser
from app.schemas.response import APIResponse
from app.services.report_generator import (
    ReportGenerator, ReportRequest, ALLOWED_REPORT_TYPES, MAX_INPUT_FIELD_LENGTH,
)
from app.services.vector_service import VectorService

router = APIRouter()
report_gen = ReportGenerator(model="internal")


class ReportGenerateRequest(BaseModel):
    report_type: str = Field(..., pattern="^(visit_summary|project_review|customer_analysis|weekly_report)$")
    context: dict = Field(default_factory=dict)
    use_rag: bool = Field(default=False)


class ReportGenerateResponse(BaseModel):
    content: str
    tokens_used: int
    model: str
    model_config = {"from_attributes": True}


@router.post("/generate", response_model=APIResponse[ReportGenerateResponse])
def generate_report(
    body: ReportGenerateRequest,
    db: Session = Depends(get_db),
    user: CurrentUser = Depends(get_current_user),
):
    """Generate an AI report. Context data is sanitized before prompt insertion."""
    # Validate context size
    ctx_size = sum(len(str(v)) for v in body.context.values())
    if ctx_size > MAX_INPUT_FIELD_LENGTH * 10:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="上下文数据过大",
        )

    request = ReportRequest(
        report_type=body.report_type,
        context=body.context,
        tenant_id=user.id,
        user_id=user.id,
    )

    if body.use_rag:
        vector_svc = VectorService(db)
        vec_results = vector_svc.search(
            query=str(body.context.get("query", "")),
            tenant_id=user.id,
            top_k=5,
        )
        result = report_gen.generate_with_vector_context(request, vec_results)
    else:
        result = report_gen.generate(request)

    return APIResponse.success(data=ReportGenerateResponse(
        content=result.content,
        tokens_used=result.tokens_used,
        model=result.model,
    ))
