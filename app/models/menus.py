from decimal import Decimal
from typing import TYPE_CHECKING, List

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base import Base
from app.database.mixins import TimestampMixin

if TYPE_CHECKING:
    from app.models import OrderMenu, Store


class Menu(Base, TimestampMixin):
    __tablename__ = "menus"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(index=True)
    image: Mapped[str] = mapped_column()
    description: Mapped[str] = mapped_column()
    price: Mapped[Decimal] = mapped_column(index=True)
    available: Mapped[bool] = mapped_column(default=True)

    store_id: Mapped[int] = mapped_column(ForeignKey("stores.id"))
    store: Mapped["Store"] = relationship(back_populates="menus")

    orders: Mapped[List["OrderMenu"]] = relationship(back_populates="menu")

    def __repr__(self) -> str:
        return f"<Menu id={self.id} name={self.name}>"
