"""投标管理 Pydantic 校验模型（v2）。"""

from datetime import date, datetime
from decimal import Decimal
from typing import List, Optional

from pydantic import BaseModel, Field, field_validator

from app.models.bidding import BIDDING_STATUSES

# ──────────────────────────── 创建 ────────────────────────────


class BiddingCreate(BaseModel):
    """创建投标项目。"""
    project_name: str = Field(..., min_length=1, max_length=200, description="项目名称")
    customer_name: str = Field(..., min_length=1, max_length=100, description="客户名称")
    amount: Decimal = Field(..., gt=0, decimal_places=2, description="项目金额（>0）")
    bid_deadline: date = Field(..., description="投标截止日期")
    status: str = Field(default="线索", max_length=20, description="初始状态，默认『线索』")
    probability: int = Field(default=0, ge=0, le=100, description="中标概率 0-100")
    competitor_info: Optional[str] = Field(default=None, description="竞争对手信息")
    notes: Optional[str] = Field(default=None, description="备注")

    @field_validator("status")
    @classmethod
    def check_status_valid(cls, v: str) -> str:
        if v not in BIDDING_STATUSES:
            raise ValueError(f"无效状态: {v}，允许: {BIDDING_STATUSES}")
        return v


# ──────────────────────────── 更新 ────────────────────────────


class BiddingUpdate(BaseModel):
    """更新投标项目 —— 所有字段可选，可同时进行状态转换。"""
    project_name: Optional[str] = Field(default=None, min_length=1, max_length=200, description="项目名称")
    customer_name: Optional[str] = Field(default=None, min_length=1, max_length=100, description="客户名称")
    amount: Optional[Decimal] = Field(default=None, gt=0, decimal_places=2, description="项目金额")
    bid_deadline: Optional[date] = Field(default=None, description="投标截止日期")
    probability: Optional[int] = Field(default=None, ge=0, le=100, description="中标概率 0-100")
    competitor_info: Optional[str] = Field(default=None, description="竞争对手信息")
    notes: Optional[str] = Field(default=None, description="备注")
    new_status: Optional[str] = Field(default=None, max_length=20, description="状态转换（需符合 9 阶段规则）")

    @field_validator("new_status")
    @classmethod
    def check_new_status_valid(cls, v: Optional[str]) -> Optional[str]:
        if v is not None and v not in BIDDING_STATUSES:
            raise ValueError(f"无效状态: {v}，允许: {BIDDING_STATUSES}")
        return v


# ──────────────────────────── 响应 ────────────────────────────


class BiddingResponse(BaseModel):
    """投标项目返回体。"""
    id: int
    project_name: str
    customer_name: str
    amount: Decimal
    bid_deadline: date
    status: str
    probability: int
    competitor_info: Optional[str] = None
    notes: Optional[str] = None
    created_at: datetime
    updated_at: Optional[datetime] = None

    model_config = {"from_attributes": True}


class BiddingListResponse(BaseModel):
    """投标项目分页列表。"""
    items: List[BiddingResponse]
    total: int
    page: int
    page_size: int


class BiddingCalendarItem(BaseModel):
    """日历视图单条 —— 近期要截止的投标。"""
    id: int
    project_name: str
    customer_name: str
    bid_deadline: date
    status: str
    days_left: int

    model_config = {"from_attributes": True}


class BiddingCalendarResponse(BaseModel):
    """日历视图列表。"""
    items: List[BiddingCalendarItem]
