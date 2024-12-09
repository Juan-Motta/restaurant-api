from dataclasses import dataclass

from fastapi import Query

from src.domain.filters.base import BaseFilter


@dataclass
class RestaurantFilter(BaseFilter):
    id: int | None = Query(None, description="Restaurant ID", ge=1)
    name: str | None = Query(
        None, description="Restaurant name", min_length=1, max_length=100
    )
    is_active: bool | None = Query(True, description="Restaurant status")
