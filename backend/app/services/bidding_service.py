"""投标管理业务逻辑 —— CRUD + 9 阶段状态机校验 + 日历视图。"""

from datetime import date, datetime, timedelta, timezone
from typing import Optional

from sqlalchemy import asc, or_
from sqlalchemy.orm import Session

from app.models.bidding import ALLOWED_TRANSITIONS, Bidding
from app.schemas.bidding import (
    BiddingCalendarItem,
    BiddingCalendarResponse,
    BiddingCreate,
    BiddingListResponse,
    BiddingResponse,
    BiddingUpdate,
)


def _build_response(instance: Bidding) -> BiddingResponse:
    """将 ORM 实例转为响应模型。"""
    return BiddingResponse.model_validate(instance)


def get_biddings(
    db: Session,
    page: int = 1,
    page_size: int = 20,
    status: Optional[str] = None,
    customer_name: Optional[str] = None,
) -> BiddingListResponse:
    """分页查询投标项目，可过滤状态/客户。"""
    query = db.query(Bidding).filter(Bidding.deleted_at.is_(None))

    if status:
        query = query.filter(Bidding.status == status)
    if customer_name:
        query = query.filter(Bidding.customer_name.like(f"%{customer_name}%"))

    total = query.count()
    items = (
        query.order_by(Bidding.updated_at.desc())
        .offset((page - 1) * page_size)
        .limit(page_size)
        .all()
    )

    return BiddingListResponse(
        items=[_build_response(it) for it in items],
        total=total,
        page=page,
        page_size=page_size,
    )


def get_bidding_by_id(db: Session, bidding_id: int) -> Optional[Bidding]:
    """按 ID 获取投标项目（排除软删除记录）。"""
    return (
        db.query(Bidding)
        .filter(Bidding.id == bidding_id, Bidding.deleted_at.is_(None))
        .first()
    )


def create_bidding(db: Session, data: BiddingCreate) -> Bidding:
    """创建投标项目。"""
    instance = Bidding(**data.model_dump())
    db.add(instance)
    db.commit()
    db.refresh(instance)
    return instance


def update_bidding(db: Session, instance: Bidding, data: BiddingUpdate) -> Bidding:
    """更新投标项目字段（不含状态）。"""
    update_data = data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(instance, field, value)
    db.commit()
    db.refresh(instance)
    return instance


def update_bidding_status(db: Session, instance: Bidding, new_status: str) -> Bidding:
    """变更投标状态 —— 根据状态机规则校验转换合法性。"""
    current = instance.status

    if current not in ALLOWED_TRANSITIONS:
        raise ValueError(f"未知当前状态: {current}")

    allowed = ALLOWED_TRANSITIONS[current]
    if new_status not in allowed:
        raise ValueError(
            f"不允许从『{current}』直接转换到『{new_status}』。"
            f"当前可转换状态: {allowed if allowed else '已是终态，不可变更'}"
        )

    instance.status = new_status
    db.commit()
    db.refresh(instance)
    return instance


def soft_delete_bidding(db: Session, instance: Bidding) -> None:
    """软删除投标项目。"""
    instance.deleted_at = datetime.now(timezone.utc)
    db.commit()


def get_bidding_calendar(db: Session, days_ahead: int = 30) -> BiddingCalendarResponse:
    """获取未来 N 天内即将截止的投标项目列表。"""
    today = date.today()
    deadline = today + timedelta(days=days_ahead)

    items = (
        db.query(Bidding)
        .filter(
            Bidding.deleted_at.is_(None),
            Bidding.bid_deadline >= today,
            Bidding.bid_deadline <= deadline,
        )
        .order_by(asc(Bidding.bid_deadline))
        .all()
    )

    result: list[BiddingCalendarItem] = []
    for it in items:
        days_left = (it.bid_deadline - today).days
        result.append(
            BiddingCalendarItem(
                id=it.id,
                project_name=it.project_name,
                customer_name=it.customer_name,
                bid_deadline=it.bid_deadline,
                status=it.status,
                days_left=days_left,
            )
        )

    return BiddingCalendarResponse(items=result)
