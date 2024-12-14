from decimal import Decimal

from fastapi import Query
from pydantic import BaseModel, model_validator


class RestaurantFilter(BaseModel):
    id: int | None = Query(None, description="Restaurant ID", ge=1)
    name: str | None = Query(
        None, description="Restaurant name", min_length=1, max_length=255
    )
    address: str | None = Query(
        None, description="Restaurant address", min_length=1, max_length=255
    )
    rating_lte: Decimal = Query(
        10.0, description="Restaurant rating lower than", le=10, ge=0
    )
    rating_gte: Decimal = Query(
        0.0, description="Restaurant rating greater than", le=10, ge=0
    )
    is_active: bool | None = Query(True, description="Restaurant status")

    @model_validator(mode="after")
    def validate_rating_values(self):
        if self.rating_lte < self.rating_gte:
            raise ValueError("rating_lte must be greater than rating_gte")
        return self
