from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field

class DecisionChainCreate(BaseModel):
    project_id: int
    name: str = Field(..., max_length=100)
    role_type: str = Field(..., max_length=50)
    department: Optional[str] = Field(None, max_length=100)
    weight: int = Field(default=5, ge=1, le=10)
    support_level: int = Field(default=0, ge=-2, le=5)
    contact_frequency: int = Field(default=7, ge=1, le=365)
    org_unit: Optional[str] = Field(None, max_length=100)
    contact_info: Optional[str] = Field(None, max_length=200)
    notes: Optional[str] = None

class DecisionChainUpdate(BaseModel):
    name: Optional[str] = Field(None, max_length=100)
    role_type: Optional[str] = Field(None, max_length=50)
    department: Optional[str] = Field(None, max_length=100)
    weight: Optional[int] = Field(None, ge=1, le=10)
    support_level: Optional[int] = Field(None, ge=-2, le=5)
    contact_frequency: Optional[int] = Field(None, ge=1, le=365)
    org_unit: Optional[str] = Field(None, max_length=100)
    contact_info: Optional[str] = Field(None, max_length=200)
    notes: Optional[str] = None

class DecisionChainResponse(BaseModel):
    id: int
    project_id: int
    name: str
    role_type: str
    department: Optional[str] = None
    weight: int
    support_level: int
    contact_frequency: Optional[int] = None
    org_unit: Optional[str] = None
    contact_info: Optional[str] = None
    notes: Optional[str] = None
    created_at: datetime
    updated_at: datetime
    model_config = {"from_attributes": True}
