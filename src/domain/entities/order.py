from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, ConfigDict, Field

from src.domain.constants.enums import OrderStatusEnum
from src.domain.entities.restaurant import RestaurantBase
from src.domain.entities.user import UserBase


class OrderBase(BaseModel):
    id: int
    status: OrderStatusEnum
    total_amount: Decimal
    delivery_address: str
    special_instructions: str
    estimated_delivery_time: datetime
    restaurant_id: int
    customer_id: int
    is_active: bool

    model_config = ConfigDict(from_attributes=True)


class OrderWithRelations(BaseModel):
    id: int
    status: OrderStatusEnum
    total_amount: Decimal
    delivery_address: str
    special_instructions: str
    estimated_delivery_time: datetime
    restaurant: RestaurantBase
    customer: UserBase
    is_active: bool

    model_config = ConfigDict(from_attributes=True)


class OrderBaseInput(BaseModel):
    status: OrderStatusEnum
    total_amount: Decimal
    delivery_address: str = Field(..., min_length=3, max_length=255)
    special_instructions: str | None = Field(..., min_length=3, max_length=255)
    estimated_delivery_time: datetime
    restaurant_id: int = Field(..., ge=1)
    customer_id: int = Field(..., ge=1)
