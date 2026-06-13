"""项目管理 API —— /api/v1/projects 路由组。"""

from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.project import (
    KanbanResponse,
    ProjectCreate,
    ProjectListResponse,
    ProjectResponse,
    ProjectStageAdvance,
    ProjectUpdate,
)
from app.schemas.response import success, error
from app.services import project_service

router = APIRouter(tags=["项目管理"])


# ──────────────────────────── POST /api/v1/projects ───────────────────────────


@router.post(
    "/api/v1/projects",
    response_model=dict,
    status_code=201,
    summary="创建项目",
    operation_id="project_create",
)
def create(
    body: ProjectCreate,
    db: Session = Depends(get_db),
):
    """新建一个项目，初始阶段默认为『初步接洽』。"""
    try:
        instance = project_service.create_project(db, body)
        return success(
            data=ProjectResponse.model_validate(instance).model_dump(),
            message="项目创建成功",
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


# ──────────────────────────── GET /api/v1/projects ────────────────────────────


@router.get(
    "/api/v1/projects",
    response_model=dict,
    summary="分页查询项目",
    operation_id="project_list",
)
def list_projects(
    page: int = Query(default=1, ge=1, description="页码"),
    page_size: int = Query(default=20, ge=1, le=100, description="每页条数"),
    stage: Optional[str] = Query(default=None, description="按阶段过滤"),
    customer_name: Optional[str] = Query(default=None, description="按客户名称模糊搜索"),
    pm_name: Optional[str] = Query(default=None, description="按项目经理模糊搜索"),
    db: Session = Depends(get_db),
):
    """分页获取项目列表，可按阶段 / 客户 / PM 过滤。"""
    result: ProjectListResponse = project_service.get_projects(
        db, page=page, page_size=page_size, stage=stage,
        customer_name=customer_name, pm_name=pm_name,
    )
    return success(data=result.model_dump(), message="查询成功")


# ──────────────────────────── GET /api/v1/projects/kanban ─────────────────────


@router.get(
    "/api/v1/projects/kanban",
    response_model=dict,
    summary="项目看板视图",
    operation_id="project_kanban",
)
def kanban(
    db: Session = Depends(get_db),
):
    """获取看板视图 —— 按 12 个阶段分组展示所有项目。"""
    result: KanbanResponse = project_service.get_kanban(db)
    return success(data=result.model_dump(), message="查询成功")


# ──────────────────────────── GET /api/v1/projects/{id} ───────────────────────


@router.get(
    "/api/v1/projects/{project_id}",
    response_model=dict,
    summary="获取项目详情",
    operation_id="project_get",
)
def get_by_id(
    project_id: int,
    db: Session = Depends(get_db),
):
    """按 ID 获取单个项目详情。"""
    instance = project_service.get_project_by_id(db, project_id)
    if not instance:
        raise HTTPException(status_code=404, detail="项目不存在")
    return success(
        data=ProjectResponse.model_validate(instance).model_dump(),
        message="查询成功",
    )


# ──────────────────────────── PUT /api/v1/projects/{id} ───────────────────────


@router.put(
    "/api/v1/projects/{project_id}",
    response_model=dict,
    summary="更新项目信息",
    operation_id="project_update",
)
def update(
    project_id: int,
    body: ProjectUpdate,
    db: Session = Depends(get_db),
):
    """更新项目基础字段。阶段变更请使用 PUT /{id}/stage。"""
    instance = project_service.get_project_by_id(db, project_id)
    if not instance:
        raise HTTPException(status_code=404, detail="项目不存在")

    try:
        instance = project_service.update_project(db, instance, body)
        return success(
            data=ProjectResponse.model_validate(instance).model_dump(),
            message="项目更新成功",
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


# ──────────────────────────── PUT /api/v1/projects/{id}/stage ─────────────────


@router.put(
    "/api/v1/projects/{project_id}/stage",
    response_model=dict,
    summary="推进项目阶段",
    operation_id="project_advance_stage",
)
def advance_stage(
    project_id: int,
    body: ProjectStageAdvance,
    db: Session = Depends(get_db),
):
    """推进项目到下一阶段（只允许向前，不允许回退）。"""
    instance = project_service.get_project_by_id(db, project_id)
    if not instance:
        raise HTTPException(status_code=404, detail="项目不存在")

    try:
        instance = project_service.advance_stage(db, instance, body.new_stage)
        return success(
            data=ProjectResponse.model_validate(instance).model_dump(),
            message=f"阶段已推进到『{body.new_stage}』",
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


# ──────────────────────────── DELETE /api/v1/projects/{id} ────────────────────


@router.delete(
    "/api/v1/projects/{project_id}",
    response_model=dict,
    summary="软删除项目",
    operation_id="project_delete",
)
def delete(
    project_id: int,
    db: Session = Depends(get_db),
):
    """软删除项目（不物理删除数据）。"""
    instance = project_service.get_project_by_id(db, project_id)
    if not instance:
        raise HTTPException(status_code=404, detail="项目不存在")

    project_service.soft_delete_project(db, instance)
    return success(data=None, message="项目已删除")
