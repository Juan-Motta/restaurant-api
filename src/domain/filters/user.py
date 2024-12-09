from dataclasses import dataclass

from fastapi import Query

from src.domain.filters.base import BaseFilter


@dataclass
class UserFilter(BaseFilter):
    id: int | None = Query(None, description="User ID", ge=1)
    first_name: str | None = Query(
        None, description="User first name", min_length=1, max_length=100
    )
    last_name: str | None = Query(
        None, description="User last name", min_length=1, max_length=100
    )
    email: str | None = Query(
        None, description="User email", min_length=1, max_length=100
    )
    is_active: bool | None = Query(True, description="User active status")
