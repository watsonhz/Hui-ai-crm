"""User schemas for auth endpoints."""

from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field


class UserLogin(BaseModel):
    username: str = Field(..., min_length=1, max_length=100)
    password: str = Field(..., min_length=1, max_length=128)


class UserCreate(BaseModel):
    username: str = Field(..., min_length=1, max_length=100)
    password: str = Field(..., min_length=8, max_length=128)
<<<<<<< HEAD
    role: str = Field(default="user", pattern="^(admin|user|readonly)$")
=======
    role: str = Field(default="user", pattern="^(admin|user|readonly|sales|manager)$")
>>>>>>> 662f12488696422c660a7b9ff57a0f880cf8e5a8


class UserResponse(BaseModel):
    id: int
    username: str
    role: str
<<<<<<< HEAD
    is_active: bool
    created_at: datetime
    updated_at: datetime
=======
    is_active: bool = True
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
>>>>>>> 662f12488696422c660a7b9ff57a0f880cf8e5a8
    model_config = {"from_attributes": True}


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
<<<<<<< HEAD
    expires_in: int  # hours
=======
    expires_in: int = 8
>>>>>>> 662f12488696422c660a7b9ff57a0f880cf8e5a8
