from decimal import Decimal

from fastapi import Query
from pydantic import BaseModel, model_validator


class MenuItemFilter(BaseModel):
    id: int | None = Query(None, description="Menu Item ID", ge=1)
    name: str | None = Query(
        None, description="Menu Item name", min_length=1, max_length=100
    )
    description: str | None = Query(
        None, description="Menu Item description", min_length=3, max_length=255
    )
    price_lte: Decimal | None = Query(None, description="Menu Item price", ge=0)
    price_gte: Decimal | None = Query(None, description="Menu Item price", ge=0)
    preparation_time_lte: int | None = Query(
        None, description="Menu Item preparation time", ge=0
    )
    preparation_time_gte: int | None = Query(
        None, description="Menu Item preparation time", ge=0
    )
    available: bool | None = Query(None, description="Menu Item availability")
    image_url: str | None = Query(
        None, description="Menu Item image URL", min_length=3, max_length=255
    )
    category_id: int | None = Query(None, description="Category ID", ge=1)
    restaurant_id: int | None = Query(None, description="Restaurant ID", ge=1)
    is_active: bool | None = Query(True, description="Menu Item status")

    @model_validator(mode="after")
    def validate_price_lte_and_gte(self):
        if self.price_lte is not None and self.price_gte is not None:
            if self.price_lte < self.price_gte:
                raise ValueError("price_lte must be greater than or equal to price_gte")
        return self

    @model_validator(mode="after")
    def validate_preparation_time_lte_and_gte(self):
        if (
            self.preparation_time_lte is not None
            and self.preparation_time_gte is not None
        ):
            if self.preparation_time_lte < self.preparation_time_gte:
                raise ValueError(
                    "preparation_time_lte must be greater than or equal to preparation_time_gte"
                )
        return self
