from decimal import Decimal

from fastapi import Query
from pydantic import BaseModel, model_validator


class RatingFilter(BaseModel):
    id: int | None = Query(None, description="Rating ID", ge=1)
    rating_lte: Decimal | None = Query(
        None, description="Restaurant rating lower than", le=10, ge=0
    )
    rating_gte: Decimal | None = Query(
        None, description="Restaurant rating greater than", le=10, ge=0
    )
    comment: str | None = Query(
        None, description="Rating comment", min_length=3, max_length=255
    )
    order_id: int | None = Query(None, description="Order ID", ge=1)
    is_active: bool | None = Query(True, description="Menu Item status")

    @model_validator(mode="after")
    def validate_rating_values(self):
        if self.rating_lte is not None and self.rating_gte is not None:
            if self.rating_lte < self.rating_gte:
                raise ValueError(
                    "rating_lte must be greater than or equal to rating_gte"
                )
        return self
