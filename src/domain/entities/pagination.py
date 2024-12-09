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
