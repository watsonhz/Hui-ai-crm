"""项目管理业务逻辑 —— CRUD + 阶段前进（只许向前）+ 看板视图。"""

from datetime import datetime, timezone
from typing import Optional

from sqlalchemy import asc
from sqlalchemy.orm import Session

from app.models.project import PROJECT_STAGES, STAGE_INDEX, Project
from app.schemas.project import (
    KanbanColumn,
    KanbanResponse,
    ProjectCreate,
    ProjectListResponse,
    ProjectResponse,
    ProjectUpdate,
)


def _build_response(instance: Project) -> ProjectResponse:
    """将 ORM 实例转为响应模型。"""
    return ProjectResponse.model_validate(instance)


def get_projects(
    db: Session,
    page: int = 1,
    page_size: int = 20,
    stage: Optional[str] = None,
    customer_name: Optional[str] = None,
    pm_name: Optional[str] = None,
) -> ProjectListResponse:
    """分页查询项目，可按阶段/客户/PM 过滤。"""
    query = db.query(Project).filter(Project.deleted_at.is_(None))

    if stage:
        query = query.filter(Project.stage == stage)
    if customer_name:
        query = query.filter(Project.customer_name.like(f"%{customer_name}%"))
    if pm_name:
        query = query.filter(Project.pm_name.like(f"%{pm_name}%"))

    total = query.count()
    items = (
        query.order_by(Project.updated_at.desc())
        .offset((page - 1) * page_size)
        .limit(page_size)
        .all()
    )

    return ProjectListResponse(
        items=[_build_response(it) for it in items],
        total=total,
        page=page,
        page_size=page_size,
    )


def get_project_by_id(db: Session, project_id: int) -> Optional[Project]:
    """按 ID 获取项目（排除软删除）。"""
    return (
        db.query(Project)
        .filter(Project.id == project_id, Project.deleted_at.is_(None))
        .first()
    )


def create_project(db: Session, data: ProjectCreate) -> Project:
    """创建项目。"""
    instance = Project(**data.model_dump())
    db.add(instance)
    db.commit()
    db.refresh(instance)
    return instance


def update_project(db: Session, instance: Project, data: ProjectUpdate) -> Project:
    """更新项目基础字段。"""
    update_data = data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(instance, field, value)
    db.commit()
    db.refresh(instance)
    return instance


def advance_stage(db: Session, instance: Project, new_stage: str) -> Project:
    """推进项目阶段 —— 只允许向前（不允许回退）。"""
    current = instance.stage
    current_idx = STAGE_INDEX.get(current)
    target_idx = STAGE_INDEX.get(new_stage)

    if current_idx is None:
        raise ValueError(f"未知当前阶段: {current}")
    if target_idx is None:
        raise ValueError(f"未知目标阶段: {new_stage}")

    if target_idx <= current_idx:
        raise ValueError(
            f"阶段只允许前进，无法从『{current}』回退到『{new_stage}』。"
            f"当前之后可选: {PROJECT_STAGES[current_idx + 1:]}"
        )

    instance.stage = new_stage
    db.commit()
    db.refresh(instance)
    return instance


def soft_delete_project(db: Session, instance: Project) -> None:
    """软删除项目。"""
    instance.deleted_at = datetime.now(timezone.utc)
    db.commit()


def get_kanban(db: Session) -> KanbanResponse:
    """获取看板视图 —— 将未删除项目按 12 阶段分组。"""
    all_projects = (
        db.query(Project)
        .filter(Project.deleted_at.is_(None))
        .order_by(asc(Project.updated_at))
        .all()
    )

    # 按阶段分组
    grouped: dict[str, list[Project]] = {stage: [] for stage in PROJECT_STAGES}
    for proj in all_projects:
        if proj.stage in grouped:
            grouped[proj.stage].append(proj)

    columns: list[KanbanColumn] = []
    for stage in PROJECT_STAGES:
        items = grouped.get(stage, [])
        columns.append(
            KanbanColumn(
                stage=stage,
                count=len(items),
                items=[_build_response(p) for p in items],
            )
        )

    return KanbanResponse(columns=columns)
