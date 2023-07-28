from datetime import datetime
from typing import TYPE_CHECKING, List, Optional

from sqlalchemy import ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base import Base
from app.database.mixins import TimestampMixin

if TYPE_CHECKING:
    from app.models import Bill, Menu, OrderState, OrderType, PaymentType, Table, User


class Order(Base, TimestampMixin):
    __tablename__ = "orders"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    start_time: Mapped[datetime] = mapped_column(default=datetime.utcnow)
    end_time: Mapped[Optional[datetime]] = mapped_column()

    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    user: Mapped["User"] = relationship(back_populates="orders")

    table_id: Mapped[int] = mapped_column(ForeignKey("tables.id"))
    table: Mapped["Table"] = relationship(back_populates="orders")

    order_state_id: Mapped[int] = mapped_column(ForeignKey("order_states.id"))
    order_state: Mapped["OrderState"] = relationship(back_populates="orders")

    order_type_id: Mapped[int] = mapped_column(ForeignKey("order_types.id"))
    order_type: Mapped["OrderType"] = relationship(back_populates="orders")

    payment_type_id: Mapped[Optional[int]] = mapped_column(
        ForeignKey("payment_types.id")
    )
    payment_type: Mapped[Optional["PaymentType"]] = relationship("orders")

    bill_id: Mapped[Optional[int]] = mapped_column(ForeignKey("bills.id"))
    bill: Mapped[Optional["Bill"]] = relationship(back_populates="orders")

    menus: Mapped[List["OrderMenu"]] = relationship(back_populates="order")

    __table_args__ = (
        UniqueConstraint(
            'user_id', 'table_id', name='_unique_user_id_table_id'
        ),
    )

    def __repr__(self) -> str:
        return f"<Order id={self.id} user_id={self.user_id} table_id={self.table_id}>"


class OrderMenu(Base, TimestampMixin):
    __tablename__ = "order_menus"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    quantity: Mapped[int] = mapped_column()
    aditional: Mapped[Optional[str]] = mapped_column()

    order_id: Mapped[int] = mapped_column(ForeignKey("orders.id"))
    order: Mapped["Order"] = relationship(back_populates="menus")

    menu_id: Mapped[int] = mapped_column(ForeignKey("menus.id"))
    menu: Mapped["Menu"] = relationship(back_populates="orders")

    def __repr__(self) -> str:
        return f"<OrderMenu id={self.id} order_id={self.order_id} menu_id={self.menu_id}>"
