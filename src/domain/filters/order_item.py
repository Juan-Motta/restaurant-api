from decimal import Decimal

from fastapi import Query
from pydantic import BaseModel, model_validator


class OrderItemFilter(BaseModel):
    id: int | None = Query(None, description="Order Item ID", ge=1)
    quantity_lte: int | None = Query(None, description="Order Item quantity", ge=0)
    quantity_gte: int | None = Query(None, description="Order Item quantity", ge=0)
    sub_total_lte: Decimal | None = Query(
        None, description="Order Item sub total", ge=0
    )
    sub_total_gte: Decimal | None = Query(
        None, description="Order Item sub total", ge=0
    )
    total_lte: Decimal | None = Query(None, description="Order Item total", ge=0)
    total_gte: Decimal | None = Query(None, description="Order Item total", ge=0)
    notes: str | None = Query(
        None, description="Order Item notes", min_length=3, max_length=255
    )
    order_id: int | None = Query(None, description="Order ID", ge=1)
    menu_item_id: int | None = Query(None, description="Menu Item ID", ge=1)
    is_active: bool | None = Query(True, description="Menu Item status")

    @model_validator(mode="after")
    def validate_quantity_lte_and_gte(self):
        if self.quantity_lte is not None and self.quantity_gte is not None:
            if self.quantity_lte < self.quantity_gte:
                raise ValueError(
                    "quantity_lte must be greater than or equal to quantity_gte"
                )
        return self

    @model_validator(mode="after")
    def validate_sub_total_lte_and_gte(self):
        if self.sub_total_lte is not None and self.sub_total_gte is not None:
            if self.sub_total_lte < self.sub_total_gte:
                raise ValueError(
                    "sub_total_lte must be greater than or equal to sub_total_gte"
                )
        return self

    @model_validator(mode="after")
    def validate_total_lte_and_gte(self):
        if self.total_lte is not None and self.total_gte is not None:
            if self.total_lte < self.total_gte:
                raise ValueError("total_lte must be greater than or equal to total_gte")
        return self
