from dataclasses import dataclass

from fastapi import Query

from src.domain.filters.base import BaseFilter


@dataclass
class MenuItemFilter(BaseFilter):
    id: int | None = Query(None, description="Menu Item ID", ge=1)
    name: str | None = Query(
        None, description="Menu Item name", min_length=1, max_length=100
    )
    restaurant_id: int | None = Query(None, description="Restaurant ID", ge=1)
    is_active: bool | None = Query(True, description="Menu Item status")
