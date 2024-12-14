from fastapi import Query
from pydantic import BaseModel


class OrderItemFilter(BaseModel):
    order_id: int | None = Query(None, description="Order ID", ge=1)
    restaurant_id: int | None = Query(None, description="Restaurant ID", ge=1)
    is_active: bool | None = Query(True, description="Menu Item status")
