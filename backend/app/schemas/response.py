from typing import TypeVar, Generic, Optional, List
from pydantic import BaseModel

T = TypeVar("T")


class APIResponse(BaseModel, Generic[T]):
    code: int = 200
    message: str = "success"
    data: Optional[T] = None

    @classmethod
    def success(cls, data=None, message: str = "success"):
        return cls(code=200, message=message, data=data)

    @classmethod
    def error(cls, message: str = "error", code: int = 400):
        return cls(code=code, message=message, data=None)


class PaginatedData(BaseModel, Generic[T]):
    items: List[T]
    total: int
    page: int
    page_size: int
    total_pages: int
