from typing import Optional
from pydantic import BaseModel, Field

class DictTypeCreate(BaseModel):
    dict_name: str = Field(..., max_length=100)
    dict_type: str = Field(..., max_length=100)
    status: int = Field(default=1, ge=0, le=1)
    remark: Optional[str] = Field(None, max_length=500)

class DictTypeUpdate(BaseModel):
    dict_name: Optional[str] = Field(None, max_length=100)
    status: Optional[int] = Field(None, ge=0, le=1)
    remark: Optional[str] = Field(None, max_length=500)

class DictDataCreate(BaseModel):
    dict_type: str = Field(..., max_length=100)
    dict_label: str = Field(..., max_length=100)
    dict_value: str = Field(..., max_length=100)
    sort_order: int = Field(default=0)
    status: int = Field(default=1, ge=0, le=1)
    remark: Optional[str] = Field(None, max_length=500)
    css_class: Optional[str] = Field(None, max_length=100)
