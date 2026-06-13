from datetime import datetime, timezone, timedelta
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import desc, asc

from app.core.database import get_db
from app.models.bidding import Bidding, BID_STATUS_MAP
from app.schemas.bidding import BiddingCreate, BiddingUpdate, BiddingResponse
from app.schemas.response import APIResponse, PaginatedData

router = APIRouter()


@router.post("/", response_model=APIResponse[BiddingResponse])
def create_bidding(body: BiddingCreate, db: Session = Depends(get_db)):
    bidding = Bidding(**body.model_dump())
    db.add(bidding)
    db.commit()
    db.refresh(bidding)
    return APIResponse.success(data=BiddingResponse.model_validate(bidding))


@router.get("/", response_model=APIResponse[PaginatedData[BiddingResponse]])
def list_biddings(
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=20, ge=1, le=100),
    sort_order: str = Query(default="desc", pattern="^(asc|desc)$"),
    bid_status: Optional[int] = Query(None, ge=1, le=9),
    search: Optional[str] = None,
    db: Session = Depends(get_db),
):
    q = db.query(Bidding).filter(Bidding.deleted_at.is_(None))
    if bid_status is not None:
        q = q.filter(Bidding.bid_status == bid_status)
    if search:
        q = q.filter(Bidding.title.ilike(f"%{search}%"))
    order_fn = desc if sort_order == "desc" else asc
    q = q.order_by(order_fn(Bidding.created_at))
    total = q.count()
    items = q.offset((page - 1) * page_size).limit(page_size).all()
    return APIResponse.success(data=PaginatedData(
        items=[BiddingResponse.model_validate(i) for i in items],
        total=total, page=page, page_size=page_size,
        total_pages=(total + page_size - 1) // page_size,
    ))


@router.get("/{bidding_id}", response_model=APIResponse[BiddingResponse])
def get_bidding(bidding_id: int, db: Session = Depends(get_db)):
    bidding = db.query(Bidding).filter(
        Bidding.id == bidding_id, Bidding.deleted_at.is_(None)
    ).first()
    if not bidding:
        raise HTTPException(status_code=404, detail="投标记录不存在")
    return APIResponse.success(data=BiddingResponse.model_validate(bidding))


@router.put("/{bidding_id}", response_model=APIResponse[BiddingResponse])
def update_bidding(bidding_id: int, body: BiddingUpdate, db: Session = Depends(get_db)):
    bidding = db.query(Bidding).filter(
        Bidding.id == bidding_id, Bidding.deleted_at.is_(None)
    ).first()
    if not bidding:
        raise HTTPException(status_code=404, detail="投标记录不存在")
    if body.bid_status is not None and body.bid_status != bidding.bid_status:
        if not bidding.can_transition_to(body.bid_status):
            raise HTTPException(
                status_code=400,
                detail=f"不允许从 {bidding.bid_status}({BID_STATUS_MAP[bidding.bid_status]}) "
                       f"转换到 {body.bid_status}({BID_STATUS_MAP[body.bid_status]})",
            )
    for k, v in body.model_dump(exclude_unset=True).items():
        setattr(bidding, k, v)
    bidding.updated_at = datetime.now(timezone.utc)
    db.commit()
    db.refresh(bidding)
    return APIResponse.success(data=BiddingResponse.model_validate(bidding))


@router.get("/calendar/upcoming", response_model=APIResponse[list[BiddingResponse]])
def calendar_upcoming(days: int = Query(default=30, ge=1, le=365), db: Session = Depends(get_db)):
    now = datetime.now(timezone.utc)
    limit = now + timedelta(days=days)
    items = (
        db.query(Bidding)
        .filter(
            Bidding.deleted_at.is_(None),
            Bidding.bid_deadline.isnot(None),
            Bidding.bid_deadline >= now,
            Bidding.bid_deadline <= limit,
        )
        .order_by(asc(Bidding.bid_deadline))
        .limit(100)
        .all()
    )
    return APIResponse.success(data=[BiddingResponse.model_validate(i) for i in items])
