from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, Field

class OrganizationCreate(BaseModel):
    name: str = Field(..., max_length=200)
    parent_id: Optional[int] = None
    org_type: str = Field(default="dept", pattern="^(company|dept|team)$")
    description: Optional[str] = None
    manager_id: Optional[int] = None
    sort_order: int = Field(default=0, ge=0)

class OrganizationUpdate(BaseModel):
    name: Optional[str] = Field(None, max_length=200)
    parent_id: Optional[int] = None
    org_type: Optional[str] = Field(None, pattern="^(company|dept|team)$")
    description: Optional[str] = None
    manager_id: Optional[int] = None
    sort_order: Optional[int] = Field(None, ge=0)

class OrganizationResponse(BaseModel):
    id: int
    name: str
    parent_id: Optional[int] = None
    org_type: str
    description: Optional[str] = None
    manager_id: Optional[int] = None
    sort_order: int
    created_at: datetime
    updated_at: datetime
    model_config = {"from_attributes": True}

class OrganizationTreeNode(BaseModel):
    id: int
    name: str
    org_type: str
    parent_id: Optional[int] = None
    sort_order: int
    children: List["OrganizationTreeNode"] = []
