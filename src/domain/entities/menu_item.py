from decimal import Decimal

from pydantic import BaseModel, ConfigDict, Field


class MenuItemBase(BaseModel):
    id: int
    name: str
    description: str
    price: Decimal
    preparation_time: int
    available: bool
    image_url: str
    is_active: bool

    model_config = ConfigDict(from_attributes=True)


class MenuItemWithRelations(BaseModel):
    id: int
    name: str
    description: str
    price: Decimal
    preparation_time: int
    available: bool
    image_url: str
    category_id: int
    restaurant_id: int
    is_active: bool

    model_config = ConfigDict(from_attributes=True)


class MenuItemBaseInput(BaseModel):
    name: str = Field(..., min_length=3, max_length=100)
    description: str = Field(..., min_length=3, max_length=255)
    price: Decimal = Field(..., ge=0)
    preparation_time: int = Field(..., ge=-0)
    available: bool = Field(True)
    image_url: str = Field(..., min_length=3, max_length=255)
    category_id: int = Field(..., ge=1)
    restaurant_id: int = Field(..., ge=1)
