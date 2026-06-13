"""项目管理 Pydantic 校验模型（v2）。"""

from datetime import date, datetime
from decimal import Decimal
from typing import List, Optional

from pydantic import BaseModel, Field, field_validator

from app.models.project import PROJECT_STAGES

# ──────────────────────────── 创建 ────────────────────────────


class ProjectCreate(BaseModel):
    """创建项目请求。"""
    project_name: str = Field(..., min_length=1, max_length=200, description="项目名称")
    customer_name: str = Field(..., min_length=1, max_length=100, description="客户名称")
    pm_name: str = Field(..., min_length=1, max_length=50, description="项目经理")
    stage: str = Field(default="初步接洽", max_length=20, description="当前阶段")
    progress: int = Field(default=0, ge=0, le=100, description="进度 0-100")
    start_date: date = Field(..., description="开始日期")
    expected_end_date: date = Field(..., description="预计结束日期")
    actual_end_date: Optional[date] = Field(default=None, description="实际结束日期")
    amount: Decimal = Field(default=Decimal("0.00"), ge=0, decimal_places=2, description="项目金额")
    notes: Optional[str] = Field(default=None, description="备注")

    @field_validator("stage")
    @classmethod
    def check_stage_valid(cls, v: str) -> str:
        if v not in PROJECT_STAGES:
            raise ValueError(f"无效阶段: {v}，允许: {PROJECT_STAGES}")
        return v


# ──────────────────────────── 更新 ────────────────────────────


class ProjectUpdate(BaseModel):
    """更新项目字段 —— 所有可选。"""
    project_name: Optional[str] = Field(default=None, min_length=1, max_length=200)
    customer_name: Optional[str] = Field(default=None, min_length=1, max_length=100)
    pm_name: Optional[str] = Field(default=None, min_length=1, max_length=50)
    progress: Optional[int] = Field(default=None, ge=0, le=100, description="进度 0-100")
    start_date: Optional[date] = Field(default=None, description="开始日期")
    expected_end_date: Optional[date] = Field(default=None, description="预计结束日期")
    actual_end_date: Optional[date] = Field(default=None, description="实际结束日期")
    amount: Optional[Decimal] = Field(default=None, ge=0, decimal_places=2, description="项目金额")
    notes: Optional[str] = Field(default=None, description="备注")


class ProjectStageAdvance(BaseModel):
    """阶段前进请求 —— 只允许向前流转。"""
    new_stage: str = Field(..., max_length=20, description="目标阶段")

    @field_validator("new_stage")
    @classmethod
    def check_stage_valid(cls, v: str) -> str:
        if v not in PROJECT_STAGES:
            raise ValueError(f"无效阶段: {v}，允许: {PROJECT_STAGES}")
        return v


# ──────────────────────────── 响应 ────────────────────────────


class ProjectResponse(BaseModel):
    """项目返回体。"""
    id: int
    project_name: str
    customer_name: str
    pm_name: str
    stage: str
    progress: int
    start_date: date
    expected_end_date: date
    actual_end_date: Optional[date] = None
    amount: Decimal
    notes: Optional[str] = None
    created_at: datetime
    updated_at: Optional[datetime] = None

    model_config = {"from_attributes": True}


class ProjectListResponse(BaseModel):
    """项目分页列表。"""
    items: List[ProjectResponse]
    total: int
    page: int
    page_size: int


class KanbanColumn(BaseModel):
    """看板列 —— 一个阶段下的项目列表。"""
    stage: str
    count: int
    items: List[ProjectResponse]


class KanbanResponse(BaseModel):
    """看板视图 —— 按 12 阶段分组的项目。"""
    columns: List[KanbanColumn]
