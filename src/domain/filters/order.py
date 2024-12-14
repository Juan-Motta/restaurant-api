from fastapi import Query
from pydantic import BaseModel


class OrderFilter(BaseModel):
    id: int | None = Query(None, description="Order ID", ge=1)
    is_active: bool | None = Query(True, description="Order active status")
