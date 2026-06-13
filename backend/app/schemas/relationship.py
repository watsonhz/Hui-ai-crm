from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field

class RelationshipCreate(BaseModel):
    customer_id: int
    contact_name: str = Field(..., max_length=100)
    contact_role: Optional[str] = Field(None, max_length=50)
    relationship_level: int = Field(default=3, ge=1, le=5)
    warmth: int = Field(default=0, ge=-2, le=2)
    last_contact_date: Optional[datetime] = None
    notes: Optional[str] = None

class RelationshipUpdate(BaseModel):
    contact_name: Optional[str] = Field(None, max_length=100)
    contact_role: Optional[str] = Field(None, max_length=50)
    relationship_level: Optional[int] = Field(None, ge=1, le=5)
    warmth: Optional[int] = Field(None, ge=-2, le=2)
    last_contact_date: Optional[datetime] = None
    notes: Optional[str] = None

class RelationshipResponse(BaseModel):
    id: int
    customer_id: int
    contact_name: str
    contact_role: Optional[str] = None
    relationship_level: int
    warmth: int
    last_contact_date: Optional[datetime] = None
    notes: Optional[str] = None
    created_at: datetime
    updated_at: datetime
    model_config = {"from_attributes": True}
