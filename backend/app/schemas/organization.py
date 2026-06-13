"""组织架构 Pydantic 校验模型（v2）。"""

from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, Field, field_validator


# ──────────────────────────── 创建 ────────────────────────────


class OrgCreate(BaseModel):
    """创建组织节点。"""
    name: str = Field(..., min_length=1, max_length=100, description="组织名称")
    parent_id: Optional[int] = Field(default=None, description="上级组织 ID")
    level: int = Field(..., ge=1, le=3, description="层级: 1=大区, 2=省, 3=市")
    sort_order: int = Field(default=0, ge=0, description="排序序号")
    is_active: bool = Field(default=True, description="是否启用")


# ──────────────────────────── 更新 ────────────────────────────


class OrgUpdate(BaseModel):
    """更新组织节点 —— 所有可选。"""
    name: Optional[str] = Field(default=None, min_length=1, max_length=100, description="组织名称")
    parent_id: Optional[int] = Field(default=None, description="上级组织 ID")
    level: Optional[int] = Field(default=None, ge=1, le=3, description="层级")
    sort_order: Optional[int] = Field(default=None, ge=0, description="排序序号")
    is_active: Optional[bool] = Field(default=None, description="是否启用")


# ──────────────────────────── 响应 ────────────────────────────


class OrgResponse(BaseModel):
    """组织节点返回体 —— 含直接子节点列表（用于树形展示）。"""
    id: int
    name: str
    parent_id: Optional[int] = None
    level: int
    sort_order: int
    is_active: bool
    children: List["OrgResponse"] = []
    created_at: datetime
    updated_at: Optional[datetime] = None

    model_config = {"from_attributes": True}


class OrgTreeResponse(BaseModel):
    """组织树完整结构 —— 从根节点开始的嵌套树。"""
    tree: List[OrgResponse]
