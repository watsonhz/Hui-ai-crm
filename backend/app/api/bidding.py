"""投标管理 API —— /api/v1/bidding 路由组。"""

from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.bidding import (
    BiddingCreate,
    BiddingCalendarResponse,
    BiddingListResponse,
    BiddingResponse,
    BiddingUpdate,
)
from app.schemas.response import success, error
from app.services import bidding_service

router = APIRouter(tags=["投标管理"])


# ──────────────────────────── POST /api/v1/bidding ────────────────────────────


@router.post(
    "/api/v1/bidding",
    response_model=dict,
    status_code=201,
    summary="创建投标项目",
    operation_id="bidding_create",
)
def create(
    body: BiddingCreate,
    db: Session = Depends(get_db),
):
    """新建一个投标项目，初始状态默认为『线索』。"""
    try:
        instance = bidding_service.create_bidding(db, body)
        return success(
            data=BiddingResponse.model_validate(instance).model_dump(),
            message="投标项目创建成功",
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


# ──────────────────────────── GET /api/v1/bidding ────────────────────────────


@router.get(
    "/api/v1/bidding",
    response_model=dict,
    summary="分页查询投标项目",
    operation_id="bidding_list",
)
def list_biddings(
    page: int = Query(default=1, ge=1, description="页码"),
    page_size: int = Query(default=20, ge=1, le=100, description="每页条数"),
    status: Optional[str] = Query(default=None, description="按状态过滤"),
    customer_name: Optional[str] = Query(default=None, description="按客户名称模糊搜索"),
    db: Session = Depends(get_db),
):
    """分页获取投标项目列表，可按状态 / 客户名称过滤。"""
    result: BiddingListResponse = bidding_service.get_biddings(
        db, page=page, page_size=page_size, status=status, customer_name=customer_name
    )
    return success(data=result.model_dump(), message="查询成功")


# ──────────────────────────── GET /api/v1/bidding/calendar ────────────────────


@router.get(
    "/api/v1/bidding/calendar",
    response_model=dict,
    summary="投标日历视图",
    operation_id="bidding_calendar",
)
def calendar(
    days: int = Query(default=30, ge=1, le=365, description="未来 N 天"),
    db: Session = Depends(get_db),
):
    """获取未来 N 天内即将截止的投标项目。"""
    result: BiddingCalendarResponse = bidding_service.get_bidding_calendar(db, days_ahead=days)
    return success(data=result.model_dump(), message="查询成功")


# ──────────────────────────── GET /api/v1/bidding/{id} ────────────────────────


@router.get(
    "/api/v1/bidding/{bidding_id}",
    response_model=dict,
    summary="获取投标项目详情",
    operation_id="bidding_get",
)
def get_by_id(
    bidding_id: int,
    db: Session = Depends(get_db),
):
    """按 ID 获取单个投标项目详情。"""
    instance = bidding_service.get_bidding_by_id(db, bidding_id)
    if not instance:
        raise HTTPException(status_code=404, detail="投标项目不存在")
    return success(
        data=BiddingResponse.model_validate(instance).model_dump(),
        message="查询成功",
    )


# ──────────────────────────── PUT /api/v1/bidding/{id} ────────────────────────


@router.put(
    "/api/v1/bidding/{bidding_id}",
    response_model=dict,
    summary="更新投标项目（含状态转换）",
    operation_id="bidding_update",
)
def update(
    bidding_id: int,
    body: BiddingUpdate,
    db: Session = Depends(get_db),
):
    """更新投标项目字段，可选同时进行状态转换（需符合 9 阶段规则）。"""
    instance = bidding_service.get_bidding_by_id(db, bidding_id)
    if not instance:
        raise HTTPException(status_code=404, detail="投标项目不存在")

    try:
        # 提取 new_status，其余字段更新
        update_data = body.model_dump(exclude_unset=True)
        new_status = update_data.pop("new_status", None)

        # 更新基础字段
        if update_data:
            instance = bidding_service.update_bidding(db, instance, BiddingUpdate(**update_data))

        # 可选状态转换
        if new_status:
            instance = bidding_service.update_bidding_status(db, instance, new_status)

        db.refresh(instance)
        return success(
            data=BiddingResponse.model_validate(instance).model_dump(),
            message="投标项目更新成功",
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


# ──────────────────────────── DELETE /api/v1/bidding/{id} ─────────────────────


@router.delete(
    "/api/v1/bidding/{bidding_id}",
    response_model=dict,
    summary="软删除投标项目",
    operation_id="bidding_delete",
)
def delete(
    bidding_id: int,
    db: Session = Depends(get_db),
):
    """软删除投标项目（不物理删除数据）。"""
    instance = bidding_service.get_bidding_by_id(db, bidding_id)
    if not instance:
        raise HTTPException(status_code=404, detail="投标项目不存在")

    bidding_service.soft_delete_bidding(db, instance)
    return success(data=None, message="投标项目已删除")
