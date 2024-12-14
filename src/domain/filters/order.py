from datetime import datetime
from decimal import Decimal

from fastapi import Query
from pydantic import BaseModel, model_validator

from src.domain.constants.enums import OrderStatusEnum


class OrderFilter(BaseModel):
    id: int | None = Query(None, description="Order ID", ge=1)
    status: OrderStatusEnum | None = Query(None, description="Order status")
    total_amount_lte: Decimal | None = Query(
        None, description="Order total amount lower than", ge=0
    )
    total_amount_gte: Decimal | None = Query(
        None, description="Order total amount greater than", ge=0
    )
    delivery_address: str | None = Query(
        None, description="Order delivery address", min_length=3, max_length=255
    )
    special_instructions: str | None = Query(
        None, description="Order special instructions", min_length=3, max_length=255
    )
    estimated_delivery_time_lte: datetime | None = Query(
        None, description="Order estimated delivery time"
    )
    estimated_delivery_time_gte: datetime | None = Query(
        None, description="Order estimated delivery time"
    )
    restaurant_id: int | None = Query(None, description="Restaurant ID", ge=1)
    customer_id: int | None = Query(None, description="Customer ID", ge=1)
    is_active: bool | None = Query(True, description="Order active status")

    @model_validator(mode="after")
    def validate_total_amount_values(self):
        if self.total_amount_lte is not None and self.total_amount_gte is not None:
            if self.total_amount_lte < self.total_amount_gte:
                raise ValueError(
                    "total_amount_lte must be greater than total_amount_gte"
                )
        return self

    @model_validator(mode="after")
    def validate_estimated_delivery_time_values(self):
        if (
            self.estimated_delivery_time_lte is not None
            and self.estimated_delivery_time_gte is not None
        ):
            if self.estimated_delivery_time_lte < self.estimated_delivery_time_gte:
                raise ValueError(
                    "estimated_delivery_time_lte must be greater than estimated_delivery_time_gte"
                )
        return self
