"""Unified API response schemas."""

from typing import Generic, List, Optional, TypeVar

from pydantic import BaseModel

T = TypeVar("T")


class APIResponse(BaseModel, Generic[T]):
    code: int = 200
    message: str = "success"
    data: Optional[T] = None


class PaginatedData(BaseModel, Generic[T]):
    items: List[T]
    total: int
    page: int
    page_size: int


def success(data: T, message: str = "success") -> dict:
    """Shorthand for a success response dict."""
    return {"code": 200, "message": message, "data": data}


def error(code: int, message: str) -> dict:
    """Shorthand for an error response dict."""
    return {"code": code, "message": message, "data": None}
