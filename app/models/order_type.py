from typing import TYPE_CHECKING, List

from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base import Base
from app.database.mixins import TimestampMixin

if TYPE_CHECKING:
    from app.models import Order


class OrderType(Base, TimestampMixin):
    __tablename__ = "order_types"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(index=True)

    orders: Mapped[List["Order"]] = relationship(back_populates="order_type")

    def __repr__(self) -> str:
        return f"<OrderType id={self.id} name={self.name}>"
