from decimal import Decimal

from fastapi import Query
from pydantic import BaseModel, model_validator

from src.domain.constants.enums import RestaurantStatusEnum


class RestaurantFilter(BaseModel):
    id: int | None = Query(None, description="Restaurant ID", ge=1)
    name: str | None = Query(
        None, description="Restaurant name", min_length=1, max_length=255
    )
    address: str | None = Query(
        None, description="Restaurant address", min_length=1, max_length=255
    )
    rating_lte: Decimal | None = Query(
        None, description="Restaurant rating lower than", le=10, ge=0
    )
    rating_gte: Decimal | None = Query(
        None, description="Restaurant rating greater than", le=10, ge=0
    )
    status: RestaurantStatusEnum | None = Query(None, description="Restaurant status")
    latitude_lte: Decimal | None = Query(
        None, description="Restaurant latitude lower than", le=90, ge=-90
    )
    latitude_gte: Decimal | None = Query(
        None, description="Restaurant latitude greater than", le=90, ge=-90
    )
    longitude_lte: Decimal | None = Query(
        None, description="Restaurant longitude lower than", le=180, ge=-180
    )
    longitude_gte: Decimal | None = Query(
        None, description="Restaurant longitude greater than", le=180, ge=-180
    )
    category_id: int | None = Query(None, description="Restaurant category ID", ge=1)
    is_active: bool | None = Query(True, description="Restaurant status")

    @model_validator(mode="after")
    def validate_rating_values(self):
        if self.rating_lte is not None and self.rating_gte is not None:
            if self.rating_lte < self.rating_gte:
                raise ValueError(
                    "rating_lte must be greater than or equal to rating_gte"
                )
        return self

    @model_validator(mode="after")
    def validate_latitude_values(self):
        if self.latitude_lte is not None and self.latitude_gte is not None:
            if self.latitude_lte < self.latitude_gte:
                raise ValueError(
                    "latitude_lte must be greater than or equal to latitude_gte"
                )
        return self

    @model_validator(mode="after")
    def validate_longitude_values(self):
        if self.longitude_lte is not None and self.longitude_gte is not None:
            if self.longitude_lte < self.longitude_gte:
                raise ValueError(
                    "longitude_lte must be greater than or equal to longitude_gte"
                )
        return self
