from dataclasses import dataclass

from fastapi import Query

from src.domain.filters.base import BaseFilter


@dataclass
class OrderFilter(BaseFilter):
    id: int | None = Query(None, description="Order ID", ge=1)
    is_active: bool | None = Query(True, description="Order active status")
