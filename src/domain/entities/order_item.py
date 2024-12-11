from decimal import Decimal

from pydantic import BaseModel, ConfigDict, Field

from src.domain.entities.menu_item import MenuItemBase
from src.domain.entities.order import OrderBase


class OrderItemBase(BaseModel):
    id: int
    quantity: int
    sub_total: Decimal
    total: Decimal
    notes: str
    order_id: int
    menu_item_id: int
    is_active: bool

    model_config = ConfigDict(from_attributes=True)


class OrderItemWithRelations(BaseModel):
    id: int
    quantity: int
    sub_total: Decimal
    total: Decimal
    notes: str
    order: OrderBase
    menu_item: MenuItemBase
    is_active: bool

    model_config = ConfigDict(from_attributes=True)


class OrderItemBaseInput(BaseModel):
    quantity: int = Field(..., ge=0)
    sub_total: Decimal = Field(..., ge=0)
    total: Decimal = Field(..., ge=0)
    notes: str = Field(..., min_length=3, max_length=255)
    order_id: int = Field(..., ge=1)
    menu_item_id: int = Field(..., ge=1)
