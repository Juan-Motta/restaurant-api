from decimal import Decimal

from pydantic import BaseModel, ConfigDict, Field

from src.domain.entities.order import OrderBase


class RatingBase(BaseModel):
    id: int
    rating: Decimal
    comment: str
    order_id: int
    is_active: bool

    model_config = ConfigDict(from_attributes=True)


class RatingWithRelations(BaseModel):
    id: int
    rating: Decimal
    comment: str
    order: OrderBase
    is_active: bool

    model_config = ConfigDict(from_attributes=True)


class RatingBaseInput(BaseModel):
    rating: Decimal = Field(..., ge=0, le=10)
    comment: str = Field(..., min_length=3, max_length=255)
    order_id: int = Field(..., ge=1)
