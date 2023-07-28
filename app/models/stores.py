from typing import TYPE_CHECKING, List, Optional

from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base import Base
from app.database.mixins import TimestampMixin

if TYPE_CHECKING:
    from app.models import License, Menu, Table, UserStore


class Store(Base, TimestampMixin):
    __tablename__ = "stores"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(index=True, unique=True)
    image: Mapped[str] = mapped_column()
    address: Mapped[str] = mapped_column()
    phone: Mapped[str] = mapped_column()
    description: Mapped[str] = mapped_column()

    users: Mapped[List["UserStore"]] = relationship(back_populates="store")
    tables: Mapped[List["Table"]] = relationship(back_populates="store")
    menus: Mapped[List["Menu"]] = relationship(back_populates="store")
    license: Mapped[Optional["License"]] = relationship(back_populates="store")

    def __repr__(self) -> str:
        return f"<Store id={self.id} name={self.name}>"
