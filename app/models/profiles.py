from typing import TYPE_CHECKING, List

from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base import Base
from app.database.mixins import TimestampMixin

if TYPE_CHECKING:
    from app.models import UserProfile


class Profile(Base, TimestampMixin):
    __tablename__ = "profiles"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(index=True)

    users: Mapped[List["UserProfile"]] = relationship(back_populates="profile")

    def __repr__(self) -> str:
        return f"<Profile id={self.id} name={self.name}>"
