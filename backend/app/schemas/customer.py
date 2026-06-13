"""Customer Pydantic v2 schemas for request validation and response serialization."""

from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, EmailStr, Field, model_validator


class CustomerCreate(BaseModel):
    """Schema for creating a new customer."""

    name: str = Field(..., min_length=1, max_length=100, description="客户名称")
    company: Optional[str] = Field(None, max_length=200, description="公司名称")
    contact: Optional[str] = Field(None, max_length=50, description="联系人")
    phone: Optional[str] = Field(
        None,
        max_length=20,
        pattern=r"^1[3-9]\d{9}$",
        description="手机号码 (中国大陆)",
    )
    email: Optional[EmailStr] = Field(None, max_length=100, description="邮箱地址")
    industry: Optional[str] = Field(None, max_length=50, description="行业")
    level: Optional[str] = Field(
        None, pattern=r"^[ABCD]$", description="客户等级 (A/B/C/D)"
    )
    source: Optional[str] = Field(None, max_length=50, description="客户来源")
    address: Optional[str] = Field(None, max_length=500, description="地址")
    notes: Optional[str] = Field(None, description="备注")


class CustomerUpdate(BaseModel):
    """Schema for updating an existing customer. All fields optional."""

    name: Optional[str] = Field(None, min_length=1, max_length=100, description="客户名称")
    company: Optional[str] = Field(None, max_length=200, description="公司名称")
    contact: Optional[str] = Field(None, max_length=50, description="联系人")
    phone: Optional[str] = Field(
        None,
        max_length=20,
        pattern=r"^1[3-9]\d{9}$",
        description="手机号码 (中国大陆)",
    )
    email: Optional[EmailStr] = Field(None, max_length=100, description="邮箱地址")
    industry: Optional[str] = Field(None, max_length=50, description="行业")
    level: Optional[str] = Field(
        None, pattern=r"^[ABCD]$", description="客户等级 (A/B/C/D)"
    )
    status: Optional[str] = Field(
        None, pattern=r"^(active|inactive)$", description="状态 (active/inactive)"
    )
    source: Optional[str] = Field(None, max_length=50, description="客户来源")
    address: Optional[str] = Field(None, max_length=500, description="地址")
    notes: Optional[str] = Field(None, description="备注")


class CustomerResponse(BaseModel):
    """Schema for customer response data."""

    id: int
    name: str
    company: Optional[str] = None
    contact: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[str] = None
    industry: Optional[str] = None
    level: str
    status: str
    source: Optional[str] = None
    address: Optional[str] = None
    notes: Optional[str] = None
    created_at: datetime
    updated_at: Optional[datetime] = None

    model_config = {"from_attributes": True}


class CustomerListResponse(BaseModel):
    """Schema for paginated customer list response."""

    items: List[CustomerResponse]
    total: int
    page: int
    page_size: int
