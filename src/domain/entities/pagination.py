from typing import Generic, TypeVar

from pydantic import BaseModel

T = TypeVar("T", bound=BaseModel)


class Page(BaseModel, Generic[T]):
    data: list[T] | None = None
    size: int
    page: int
    pages: int
    total: int
    has_next: bool
    has_previous: bool
