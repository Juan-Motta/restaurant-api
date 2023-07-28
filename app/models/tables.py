from typing import TYPE_CHECKING, List

from sqlalchemy import ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base import Base
from app.database.mixins import TimestampMixin

if TYPE_CHECKING:
    from app.models import Order, Store


class Table(Base, TimestampMixin):
    __tablename__ = "tables"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    number: Mapped[str] = mapped_column(index=True)
    code: Mapped[str] = mapped_column(index=True)

    store_id: Mapped[int] = mapped_column(ForeignKey("stores.id"))
    store: Mapped["Store"] = relationship(back_populates="tables")

    orders: Mapped[List["Order"]] = relationship(back_populates="table")

    __table_args__ = (
        UniqueConstraint(
            "number", "code", "store_id", name="_unique_number_code_store_id"
        ),
    )

    def __repr__(self) -> str:
        return f"<Table id={self.id} store_id={self.store_id}>"
