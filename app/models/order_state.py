from typing import TYPE_CHECKING, List

from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base import Base
from app.database.mixins import TimestampMixin

if TYPE_CHECKING:
    from app.models import Order


class OrderState(Base, TimestampMixin):
    __tablename__ = "order_states"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(index=True, unique=True)

    orders: Mapped[List["Order"]] = relationship(back_populates="order_state")

    def __repr__(self) -> str:
        return f"<OrderState id={self.id} name={self.name}>"
