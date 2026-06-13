from datetime import datetime, date
from typing import Optional
from pydantic import BaseModel, Field

class AcceptanceCreate(BaseModel):
    project_id: int
    title: str = Field(..., max_length=200)
    acceptance_date: Optional[date] = None
    status: int = Field(default=1, ge=1, le=5)
    result: Optional[str] = None
    reviewer: Optional[str] = Field(None, max_length=100)
    notes: Optional[str] = None

class AcceptanceUpdate(BaseModel):
    title: Optional[str] = Field(None, max_length=200)
    acceptance_date: Optional[date] = None
    status: Optional[int] = Field(None, ge=1, le=5)
    result: Optional[str] = None
    reviewer: Optional[str] = Field(None, max_length=100)
    notes: Optional[str] = None

class AcceptanceResponse(BaseModel):
    id: int
    project_id: int
    title: str
    acceptance_date: Optional[date] = None
    status: int
    result: Optional[str] = None
    reviewer: Optional[str] = None
    notes: Optional[str] = None
    created_at: datetime
    updated_at: datetime
    model_config = {"from_attributes": True}
