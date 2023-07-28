from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base import Base
from app.database.mixins import TimestampMixin

if TYPE_CHECKING:
    from app.models import License, PaymentState, PaymentType, User


class Payment(Base, TimestampMixin):
    __tablename__ = "payments"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    payment_date: Mapped[datetime] = mapped_column(default=datetime.utcnow)

    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    user: Mapped["User"] = relationship(back_populates="payments")

    payment_state_id: Mapped[int] = mapped_column(
        ForeignKey("payment_states.id")
    )
    payment_state: Mapped["PaymentState"] = relationship(
        back_populates="payments"
    )

    license_id: Mapped[int] = mapped_column(ForeignKey("licenses.id"))
    license: Mapped["License"] = relationship(back_populates="payments")

    payment_type_id: Mapped[int] = mapped_column(
        ForeignKey("payment_types.id")
    )
    payment_type: Mapped["PaymentType"] = relationship(
        back_populates="payments"
    )

    def __repr__(self) -> str:
        return f"<Payment id={self.id} user_id={self.user_id} license_id={self.license_id}>"
