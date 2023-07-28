from datetime import datetime
from decimal import Decimal
from typing import TYPE_CHECKING, List

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base import Base
from app.database.mixins import TimestampMixin

if TYPE_CHECKING:
    from app.models import Order, PaymentType


class Bill(Base, TimestampMixin):
    __tablename__ = "bills"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    serial: Mapped[str] = mapped_column(index=True, unique=True)
    total: Mapped[Decimal] = mapped_column()
    sub_total: Mapped[Decimal] = mapped_column()
    iva: Mapped[Decimal] = mapped_column()
    ipocon: Mapped[Decimal] = mapped_column()
    tip: Mapped[Decimal] = mapped_column()
    date: Mapped[datetime] = mapped_column(default=datetime.utcnow)

    payment_type_id: Mapped[int] = mapped_column(
        ForeignKey("payment_types.id")
    )
    payment_type: Mapped["PaymentType"] = relationship(back_populates="bills")

    orders: Mapped[List["Order"]] = relationship(back_populates="bill")

    def __repr__(self) -> str:
        return f"<Bill id={self.id} serial={self.serial}>"
