from datetime import date, datetime
from typing import List, Optional
from pydantic import BaseModel, Field

class ProjectCreate(BaseModel):
    name: str = Field(..., max_length=200)
    description: Optional[str] = None
    stage: int = Field(default=1, ge=1, le=12)
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    budget: Optional[float] = Field(None, ge=0)
    actual_cost: Optional[float] = Field(None, ge=0)
    manager_id: Optional[int] = None
    org_id: Optional[int] = None

class ProjectStageUpdate(BaseModel):
    stage: int = Field(..., ge=1, le=12)

class ProjectUpdate(BaseModel):
    name: Optional[str] = Field(None, max_length=200)
    description: Optional[str] = None
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    budget: Optional[float] = Field(None, ge=0)
    actual_cost: Optional[float] = Field(None, ge=0)
    manager_id: Optional[int] = None
    org_id: Optional[int] = None

class ProjectResponse(BaseModel):
    id: int
    name: str
    description: Optional[str] = None
    stage: int
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    budget: Optional[float] = None
    actual_cost: Optional[float] = None
    manager_id: Optional[int] = None
    org_id: Optional[int] = None
    created_at: datetime
    updated_at: datetime
    model_config = {"from_attributes": True}

class ProjectListQuery(BaseModel):
    page: int = Field(default=1, ge=1)
    page_size: int = Field(default=20, ge=1, le=100)
    sort_order: str = Field(default="desc", pattern="^(asc|desc)$")
    stage: Optional[int] = Field(None, ge=1, le=12)
    search: Optional[str] = None

class KanbanView(BaseModel):
    stage: int
    stage_name: str
    count: int
    items: List[ProjectResponse]
