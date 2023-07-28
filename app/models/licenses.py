from datetime import datetime
from decimal import Decimal
from typing import TYPE_CHECKING, List

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base import Base
from app.database.mixins import TimestampMixin

if TYPE_CHECKING:
    from app.models import Payment, Store


class License(Base, TimestampMixin):
    __tablename__ = "licenses"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    expire_date: Mapped[datetime] = mapped_column()

    store_id: Mapped[int] = mapped_column(ForeignKey("stores.id"))
    store: Mapped["Store"] = relationship(back_populates="license")

    payments: Mapped[List["Payment"]] = relationship(back_populates="licenses")

    def __repr__(self) -> str:
        return f"<License id={self.id} expire_date={self.expire_date}>"
