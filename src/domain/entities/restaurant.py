from decimal import Decimal

from pydantic import BaseModel, ConfigDict, Field

from src.domain.constants.enums import RestaurantStatusEnum


class RestaurantBase(BaseModel):
    id: int
    name: str
    address: str
    rating: Decimal | None = None
    status: RestaurantStatusEnum
    latitude: Decimal
    longitude: Decimal
    category_id: int
    is_active: bool

    model_config = ConfigDict(from_attributes=True)


class RestaurantWithRelations(BaseModel):
    id: int
    name: str
    address: str
    rating: Decimal | None = None
    status: RestaurantStatusEnum
    latitude: Decimal
    longitude: Decimal
    category_id: int
    is_active: bool

    model_config = ConfigDict(from_attributes=True)


class RestaurantBaseInput(BaseModel):
    name: str = Field(..., min_length=3, max_length=100)
    address: str = Field(..., min_length=3, max_length=100)
    latitude: Decimal = Field(..., gt=-90, lt=90)
    longitude: Decimal = Field(..., gt=-180, lt=180)
    category_id: int = Field(..., ge=1)
