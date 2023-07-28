from typing import TYPE_CHECKING, List

from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base import Base
from app.database.mixins import TimestampMixin

if TYPE_CHECKING:
    from app.models import Bill, Order, Payment


class PaymentType(Base, TimestampMixin):
    __tablename__ = "payment_types"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(index=True, unique=True)

    bills: Mapped[List["Bill"]] = relationship(back_populates="payment_type")
    orders: Mapped[List["Order"]] = relationship(back_populates="payment_type")

    payments: Mapped[List["Payment"]] = relationship(
        back_populates="payment_type"
    )

    def __repr__(self) -> str:
        return f"<PaymentType id={self.id} name={self.name}>"
