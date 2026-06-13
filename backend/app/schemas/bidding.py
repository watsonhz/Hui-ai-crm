from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field

class BiddingCreate(BaseModel):
    title: str = Field(..., max_length=200)
    project_name: Optional[str] = Field(None, max_length=200)
    bid_amount: Optional[float] = Field(None, ge=0)
    bid_status: int = Field(default=1, ge=1, le=9)
    bid_deadline: Optional[datetime] = None
    submit_deadline: Optional[datetime] = None
    client_company: Optional[str] = Field(None, max_length=200)
    client_contact: Optional[str] = Field(None, max_length=100)
    description: Optional[str] = None
    notes: Optional[str] = None
    owner_id: Optional[int] = None

class BiddingUpdate(BaseModel):
    title: Optional[str] = Field(None, max_length=200)
    project_name: Optional[str] = Field(None, max_length=200)
    bid_amount: Optional[float] = Field(None, ge=0)
    bid_status: Optional[int] = Field(None, ge=1, le=9)
    bid_deadline: Optional[datetime] = None
    submit_deadline: Optional[datetime] = None
    client_company: Optional[str] = Field(None, max_length=200)
    client_contact: Optional[str] = Field(None, max_length=100)
    description: Optional[str] = None
    notes: Optional[str] = None
    owner_id: Optional[int] = None

class BiddingResponse(BaseModel):
    id: int
    title: str
    project_name: Optional[str] = None
    bid_amount: Optional[float] = None
    bid_status: int
    bid_deadline: Optional[datetime] = None
    submit_deadline: Optional[datetime] = None
    client_company: Optional[str] = None
    client_contact: Optional[str] = None
    description: Optional[str] = None
    notes: Optional[str] = None
    owner_id: Optional[int] = None
    created_at: datetime
    updated_at: datetime
    model_config = {"from_attributes": True}

class BiddingListQuery(BaseModel):
    page: int = Field(default=1, ge=1)
    page_size: int = Field(default=20, ge=1, le=100)
    sort_order: str = Field(default="desc", pattern="^(asc|desc)$")
    bid_status: Optional[int] = Field(None, ge=1, le=9)
    search: Optional[str] = None
