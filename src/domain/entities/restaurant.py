from decimal import Decimal

from pydantic import BaseModel, ConfigDict

from src.domain.entities.category import Category


class RestaurantBase(BaseModel):
    id: int
    name: str
    address: str
    rating: Decimal
    status: str
    latitude: Decimal
    longitude: Decimal
    is_active: bool

    class Config:
        model_config = ConfigDict(from_attributes=True)


class RestaurantWithRelations(BaseModel):
    id: int
    name: str
    address: str
    rating: Decimal
    status: str
    latitude: Decimal
    longitude: Decimal
    category: Category
    is_active: bool

    class Config:
        model_config = ConfigDict(from_attributes=True)
