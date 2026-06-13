from __future__ import annotations

from datetime import datetime, timezone
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
from sqlalchemy import desc, asc

from app.core.database import get_db
from app.core.security import get_current_user, CurrentUser
from app.models.project import Project, STAGE_MAP
from app.schemas.project import (
    ProjectCreate, ProjectUpdate, ProjectStageUpdate,
    ProjectResponse, KanbanView,
)
from app.schemas.response import APIResponse, PaginatedData

router = APIRouter()


def _escape_like(value: str) -> str:
    """Escape SQL LIKE wildcards to prevent LIKE injection."""
    return value.replace("\\", "\\\\").replace("%", "\\%").replace("_", "\\_")


@router.post("/", response_model=APIResponse[ProjectResponse])
def create(body: ProjectCreate, db: Session = Depends(get_db), user: CurrentUser = Depends(get_current_user)):
    data = body.model_dump()
    data["manager_id"] = user.id
    project = Project(**data)
    db.add(project)
    db.commit()
    db.refresh(project)
    return APIResponse.success(data=ProjectResponse.model_validate(project))


@router.get("/", response_model=APIResponse[PaginatedData[ProjectResponse]])
def list(
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=20, ge=1, le=100),
    sort_order: str = Query(default="desc", pattern="^(asc|desc)$"),
    stage: Optional[int] = Query(None, ge=1, le=12),
    search: Optional[str] = None,
    db: Session = Depends(get_db),
    user: CurrentUser = Depends(get_current_user),
):
    q = db.query(Project).filter(Project.deleted_at.is_(None))
    if stage is not None:
        q = q.filter(Project.stage == stage)
    if search:
        q = q.filter(Project.name.ilike(f"%{_escape_like(search)}%"))
    order_fn = desc if sort_order == "desc" else asc
    q = q.order_by(order_fn(Project.created_at))
    total = q.count()
    items = q.offset((page - 1) * page_size).limit(page_size).all()
    return APIResponse.success(data=PaginatedData(
        items=[ProjectResponse.model_validate(i) for i in items],
        total=total, page=page, page_size=page_size,
        total_pages=(total + page_size - 1) // page_size,
    ))


@router.get("/{project_id}", response_model=APIResponse[ProjectResponse])
def get(project_id: int, db: Session = Depends(get_db), user: CurrentUser = Depends(get_current_user)):
    project = db.query(Project).filter(
        Project.id == project_id, Project.deleted_at.is_(None)
    ).first()
    if not project:
        raise HTTPException(status_code=404, detail="项目不存在")
    return APIResponse.success(data=ProjectResponse.model_validate(project))


@router.put("/{project_id}", response_model=APIResponse[ProjectResponse])
def update(project_id: int, body: ProjectUpdate, db: Session = Depends(get_db), user: CurrentUser = Depends(get_current_user)):
    project = db.query(Project).filter(
        Project.id == project_id, Project.deleted_at.is_(None)
    ).first()
    if not project:
        raise HTTPException(status_code=404, detail="项目不存在")
    if project.manager_id != user.id and user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="无权修改此项目",
        )
    for k, v in body.model_dump(exclude_unset=True).items():
        setattr(project, k, v)
    project.updated_at = datetime.now(timezone.utc)
    db.commit()
    db.refresh(project)
    return APIResponse.success(data=ProjectResponse.model_validate(project))


@router.put("/{project_id}/stage", response_model=APIResponse[ProjectResponse])
def update_stage(project_id: int, body: ProjectStageUpdate, db: Session = Depends(get_db), user: CurrentUser = Depends(get_current_user)):
    project = db.query(Project).filter(
        Project.id == project_id, Project.deleted_at.is_(None)
    ).first()
    if not project:
        raise HTTPException(status_code=404, detail="项目不存在")
    if project.manager_id != user.id and user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="无权修改此项目阶段",
        )
    if not project.can_transition_to(body.stage):
        raise HTTPException(
            status_code=400,
            detail="阶段转换不允许",
        )
    project.stage = body.stage
    project.updated_at = datetime.now(timezone.utc)
    db.commit()
    db.refresh(project)
    return APIResponse.success(data=ProjectResponse.model_validate(project))


@router.get("/board/kanban", response_model=APIResponse)
def kanban(db: Session = Depends(get_db), user: CurrentUser = Depends(get_current_user)):
    projects = db.query(Project).filter(Project.deleted_at.is_(None)).all()
    stage_groups: dict[int, list[ProjectResponse]] = {s: [] for s in STAGE_MAP}
    for p in projects:
        stage_groups.setdefault(p.stage, []).append(ProjectResponse.model_validate(p))
    result = [
        KanbanView(stage=s, stage_name=STAGE_MAP[s], count=len(items), items=items)
        for s, items in stage_groups.items()
    ]
    return APIResponse.success(data=result)
