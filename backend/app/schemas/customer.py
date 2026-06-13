"""Customer schemas — create / update / response / list query."""

from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field


class CustomerCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    company: Optional[str] = Field(None, max_length=200)
    industry: Optional[str] = Field(None, max_length=50)
    phone: Optional[str] = Field(None, max_length=20, pattern=r"^[+\d\- ]*$")
    email: Optional[str] = Field(None, max_length=100, pattern=r"^[^@\s]+@[^@\s]+\.[^@\s]+$")
    source: Optional[str] = Field(None, max_length=50)
    level: str = Field(default="C", pattern="^(A|B|C|D)$")
    status: str = Field(default="潜在", pattern="^(潜在|意向|谈判|成交|流失)$")
    owner_id: Optional[int] = None


class CustomerUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    company: Optional[str] = Field(None, max_length=200)
    industry: Optional[str] = Field(None, max_length=50)
    phone: Optional[str] = Field(None, max_length=20, pattern=r"^[+\d\- ]*$")
    email: Optional[str] = Field(None, max_length=100, pattern=r"^[^@\s]+@[^@\s]+\.[^@\s]+$")
    source: Optional[str] = Field(None, max_length=50)
    level: Optional[str] = Field(None, pattern="^(A|B|C|D)$")
    status: Optional[str] = Field(None, pattern="^(潜在|意向|谈判|成交|流失)$")
    owner_id: Optional[int] = None


class CustomerResponse(BaseModel):
    id: int
    name: str
    company: Optional[str] = None
    industry: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[str] = None
    source: Optional[str] = None
    level: str
    status: str
    owner_id: Optional[int] = None
    created_at: datetime
    updated_at: datetime
    model_config = {"from_attributes": True}


class CustomerListQuery(BaseModel):
    page: int = Field(default=1, ge=1)
    page_size: int = Field(default=20, ge=1, le=100)
    sort_order: str = Field(default="desc", pattern="^(asc|desc)$")
    name: Optional[str] = None
    company: Optional[str] = None
    status: Optional[str] = None
    level: Optional[str] = None
    source: Optional[str] = None
