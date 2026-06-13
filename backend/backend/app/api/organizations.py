"""组织架构 API —— /api/v1/organizations 路由组。"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.organization import (
    OrgCreate,
    OrgResponse,
    OrgTreeResponse,
    OrgUpdate,
)
from app.schemas.response import success, error
from app.services import organization_service

router = APIRouter(tags=["组织架构"])


# ──────────────────────────── POST /api/v1/organizations ──────────────────────


@router.post(
    "/api/v1/organizations",
    response_model=dict,
    status_code=201,
    summary="创建组织节点",
    operation_id="org_create",
)
def create(
    body: OrgCreate,
    db: Session = Depends(get_db),
):
    """新建一个组织节点（大区/省/市），可指定上级 parent_id 挂载到树中。"""
    try:
        instance = organization_service.create_org(db, body)
        return success(
            data=OrgResponse.model_validate(instance).model_dump(mode="json"),
            message="组织节点创建成功",
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


# ──────────────────────────── GET /api/v1/organizations/tree ──────────────────


@router.get(
    "/api/v1/organizations/tree",
    response_model=dict,
    summary="获取组织树",
    operation_id="org_tree",
)
def get_tree(
    db: Session = Depends(get_db),
):
    """获取完整组织架构树 —— 从根节点（大区）开始的嵌套结构。"""
    result: OrgTreeResponse = organization_service.get_org_tree(db)
    return success(data=result.model_dump(mode="json"), message="查询成功")


# ──────────────────────────── GET /api/v1/organizations/{id} ──────────────────


@router.get(
    "/api/v1/organizations/{org_id}",
    response_model=dict,
    summary="获取组织节点详情",
    operation_id="org_get",
)
def get_by_id(
    org_id: int,
    db: Session = Depends(get_db),
):
    """按 ID 获取单个组织节点详情（含子节点）。"""
    instance = organization_service.get_org_by_id(db, org_id)
    if not instance:
        raise HTTPException(status_code=404, detail="组织节点不存在")
    return success(
        data=OrgResponse.model_validate(instance).model_dump(mode="json"),
        message="查询成功",
    )


# ──────────────────────────── PUT /api/v1/organizations/{id} ──────────────────


@router.put(
    "/api/v1/organizations/{org_id}",
    response_model=dict,
    summary="更新组织节点",
    operation_id="org_update",
)
def update(
    org_id: int,
    body: OrgUpdate,
    db: Session = Depends(get_db),
):
    """更新组织节点的名称、层级、排序等信息。"""
    instance = organization_service.get_org_by_id(db, org_id)
    if not instance:
        raise HTTPException(status_code=404, detail="组织节点不存在")

    try:
        instance = organization_service.update_org(db, instance, body)
        return success(
            data=OrgResponse.model_validate(instance).model_dump(mode="json"),
            message="组织节点更新成功",
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


# ──────────────────────────── DELETE /api/v1/organizations/{id} ───────────────


@router.delete(
    "/api/v1/organizations/{org_id}",
    response_model=dict,
    summary="删除组织节点",
    operation_id="org_delete",
)
def delete(
    org_id: int,
    db: Session = Depends(get_db),
):
    """删除组织节点（仅当无子节点时允许删除）。"""
    instance = organization_service.get_org_by_id(db, org_id)
    if not instance:
        raise HTTPException(status_code=404, detail="组织节点不存在")

    try:
        organization_service.delete_org(db, instance)
        return success(data=None, message="组织节点已删除")
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
