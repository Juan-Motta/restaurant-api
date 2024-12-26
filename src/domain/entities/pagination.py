from typing import Generic, TypeVar

from pydantic import BaseModel

T = TypeVar("T", bound=BaseModel)


class Page(BaseModel, Generic[T]):
    data: list[T] | None = None
    size: int = 0
    page: int = 1
    pages: int = 1
    total: int = 0
    has_next: bool = False
    has_previous: bool = False


def paginate(data: list[T], page: int, size: int, total: int) -> Page[T]:
    return Page[T](
        data=data,
        size=size,
        page=page,
        pages=(total // size) + 1,
        total=total,
        has_next=page * size < total,
        has_previous=page > 1,
    )
