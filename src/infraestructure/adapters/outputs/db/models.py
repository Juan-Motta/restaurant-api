from datetime import datetime
from decimal import Decimal
from typing import Optional

import sqlalchemy as sa
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.domain.constants.enums import (
    CategoryTypologyEnum,
    OrderStatusEnum,
    RestaurantStatusEnum,
    UserTypologyEnum,
)
from src.infraestructure.adapters.outputs.db.base import Base
from src.infraestructure.adapters.outputs.db.mixins import (
    IntegerIdMixin,
    IsActiveMixin,
    TimestampMixin,
)


class RestaurantModel(IntegerIdMixin, TimestampMixin, IsActiveMixin, Base):
    __tablename__ = "restaurants"
    name: Mapped[str] = mapped_column(sa.String(255))
    address: Mapped[str] = mapped_column(sa.String(255))
    rating: Mapped[Optional[Decimal]] = mapped_column(sa.Numeric(3, 2))
    status: Mapped[RestaurantStatusEnum] = mapped_column(
        sa.Enum(
            RestaurantStatusEnum,
            native_enum=False,
            validate_strings=True,
            values_callable=lambda x: [e.value for e in x],
        ),
        default=RestaurantStatusEnum.CLOSE,
    )
    latitude: Mapped[Decimal] = mapped_column(sa.Numeric(21, 11))
    longitude: Mapped[Decimal] = mapped_column(sa.Numeric(21, 11))

    category_id: Mapped[int] = mapped_column(sa.ForeignKey("categories.id"))
    category: Mapped["CategoryModel"] = relationship(
        "CategoryModel", back_populates="restaurant"
    )

    menu_items: Mapped[list["MenuItemModel"]] = relationship(
        back_populates="restaurant"
    )
    users: Mapped[list["UserModel"]] = relationship(back_populates="restaurant")
    orders: Mapped[list["OrderModel"]] = relationship(back_populates="restaurant")


class MenuItemModel(IntegerIdMixin, TimestampMixin, IsActiveMixin, Base):
    __tablename__ = "menu_items"
    name: Mapped[str] = mapped_column(sa.String(255))
    description: Mapped[str] = mapped_column(sa.String(255))
    price: Mapped[Decimal] = mapped_column(sa.Numeric(10, 2))
    preparation_time: Mapped[int]
    available: Mapped[bool]
    image_url: Mapped[str] = mapped_column(sa.String(255))

    category_id: Mapped[int] = mapped_column(sa.ForeignKey("categories.id"))
    category: Mapped["CategoryModel"] = relationship(
        "CategoryModel", back_populates="menu_items"
    )

    restaurant_id: Mapped[int] = mapped_column(sa.ForeignKey("restaurants.id"))
    restaurant: Mapped["RestaurantModel"] = relationship(back_populates="menu_items")

    order_items: Mapped[list["OrderItemModel"]] = relationship(
        back_populates="menu_item"
    )


class UserModel(IntegerIdMixin, TimestampMixin, IsActiveMixin, Base):
    __tablename__ = "users"
    typology: Mapped[UserTypologyEnum] = mapped_column(
        sa.Enum(
            UserTypologyEnum,
            native_enum=False,
            validate_strings=True,
            values_callable=lambda x: [e.value for e in x],
        ),
        default=UserTypologyEnum.CUSTOMER,
    )
    first_name: Mapped[str] = mapped_column(sa.String(100))
    last_name: Mapped[str] = mapped_column(sa.String(100))
    email: Mapped[str] = mapped_column(sa.String(255))
    phone: Mapped[str] = mapped_column(sa.String(20))
    address: Mapped[str] = mapped_column(sa.String(255))

    restaurant_id: Mapped[int] = mapped_column(sa.ForeignKey("restaurants.id"))
    restaurant: Mapped["RestaurantModel"] = relationship(back_populates="users")

    orders: Mapped[list["OrderModel"]] = relationship(back_populates="customer")


class OrderModel(IntegerIdMixin, TimestampMixin, IsActiveMixin, Base):
    __tablename__ = "orders"
    status: Mapped[OrderStatusEnum] = mapped_column(
        sa.Enum(
            OrderStatusEnum,
            native_enum=False,
            validate_strings=True,
            values_callable=lambda x: [e.value for e in x],
        ),
        default=OrderStatusEnum.PENDING,
    )
    total_amount: Mapped[Decimal] = mapped_column(sa.Numeric(10, 2))
    delivery_address: Mapped[str] = mapped_column(sa.String(255))
    special_instructions: Mapped[str] = mapped_column(sa.String(255))
    estimated_delivery_time: Mapped[datetime] = mapped_column(
        sa.DateTime(timezone=True)
    )

    restaurant_id: Mapped[int] = mapped_column(sa.ForeignKey("restaurants.id"))
    restaurant: Mapped["RestaurantModel"] = relationship(back_populates="orders")
    customer_id: Mapped[int] = mapped_column(sa.ForeignKey("users.id"))
    customer: Mapped["UserModel"] = relationship(back_populates="orders")

    rating: Mapped["RatingModel"] = relationship(back_populates="order")
    order_items: Mapped[list["OrderItemModel"]] = relationship(back_populates="order")


class RatingModel(IntegerIdMixin, TimestampMixin, IsActiveMixin, Base):
    __tablename__ = "ratings"
    rating: Mapped[Decimal] = mapped_column(sa.Numeric(3, 2))
    comment: Mapped[str] = mapped_column(sa.String(255))

    order_id: Mapped[int] = mapped_column(sa.ForeignKey("orders.id"))
    order: Mapped["OrderModel"] = relationship(back_populates="rating")


class OrderItemModel(IntegerIdMixin, TimestampMixin, IsActiveMixin, Base):
    __tablename__ = "order_items"
    quantity: Mapped[int]
    sub_total: Mapped[Decimal] = mapped_column(sa.Numeric(10, 2))
    total: Mapped[Decimal] = mapped_column(sa.Numeric(10, 2))
    notes: Mapped[str] = mapped_column(sa.String(255))

    order_id: Mapped[int] = mapped_column(sa.ForeignKey("orders.id"))
    order: Mapped["OrderModel"] = relationship(back_populates="order_items")

    menu_item_id: Mapped[int] = mapped_column(sa.ForeignKey("menu_items.id"))
    menu_item: Mapped["MenuItemModel"] = relationship(back_populates="order_items")


class CategoryModel(IntegerIdMixin, TimestampMixin, IsActiveMixin, Base):
    __tablename__ = "categories"
    name: Mapped[str] = mapped_column(sa.String(100))
    description: Mapped[str] = mapped_column(sa.String(255))
    typology: Mapped[Optional[CategoryTypologyEnum]] = mapped_column(
        sa.Enum(
            CategoryTypologyEnum,
            native_enum=False,
            validate_strings=True,
            values_callable=lambda x: [e.value for e in x],
        ),
        default=None,
    )

    menu_items: Mapped[list["MenuItemModel"]] = relationship(
        "MenuItemModel", back_populates="category"
    )
    restaurant: Mapped[list["RestaurantModel"]] = relationship(
        "RestaurantModel", back_populates="category"
    )
