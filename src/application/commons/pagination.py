from typing import TypeVar

from pydantic import BaseModel

from src.domain.entities.pagination import Page

T = TypeVar("T", bound=BaseModel)


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
