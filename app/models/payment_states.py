from typing import TYPE_CHECKING, List

from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base import Base
from app.database.mixins import TimestampMixin

if TYPE_CHECKING:
    from app.models import Payment


class PaymentState(Base, TimestampMixin):
    __tablename__ = "payment_states"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(index=True, unique=True)

    payments: Mapped[List["Payment"]] = relationship(
        back_populates="payment_state"
    )

    def __repr__(self) -> str:
        return f"<PaymentState id={self.id} name={self.name}>"
