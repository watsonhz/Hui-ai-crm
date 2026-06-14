from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field

class CustomerCreate(BaseModel):
    name: str = Field(..., max_length=200)
    code: Optional[str] = Field(None, max_length=50)
    industry: Optional[str] = Field(None, max_length=50)
    source: Optional[str] = Field(None, max_length=50)
    level: str = Field(default="normal", pattern="^(vip|key|normal)$")
    owner_id: Optional[int] = None
    contact_name: Optional[str] = Field(None, max_length=100)
    contact_phone: Optional[str] = Field(None, max_length=30)
    contact_email: Optional[str] = Field(None, max_length=100)
    address: Optional[str] = Field(None, max_length=300)
    remark: Optional[str] = None

class CustomerUpdate(BaseModel):
    name: Optional[str] = Field(None, max_length=200)
    industry: Optional[str] = Field(None, max_length=50)
    source: Optional[str] = Field(None, max_length=50)
    level: Optional[str] = Field(None, pattern="^(vip|key|normal)$")
    owner_id: Optional[int] = None
    contact_name: Optional[str] = Field(None, max_length=100)
    contact_phone: Optional[str] = Field(None, max_length=30)
    contact_email: Optional[str] = Field(None, max_length=100)
    address: Optional[str] = Field(None, max_length=300)
    remark: Optional[str] = None
    is_active: Optional[bool] = None

class CustomerResponse(BaseModel):
    id: int
    name: str
    code: Optional[str] = None
    industry: Optional[str] = None
    source: Optional[str] = None
    level: str
    owner_id: Optional[int] = None
    contact_name: Optional[str] = None
    contact_phone: Optional[str] = None
    contact_email: Optional[str] = None
    address: Optional[str] = None
    remark: Optional[str] = None
    is_active: bool
    created_at: datetime
    updated_at: datetime
    model_config = {"from_attributes": True}
