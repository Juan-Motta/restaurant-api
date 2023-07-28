from datetime import datetime

from sqlalchemy.orm import Mapped, mapped_column

from app.database.base import Base
from app.database.mixins import TimestampMixin


class Survey(Base, TimestampMixin):
    __tablename__ = "surveys"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    date: Mapped[datetime] = mapped_column(default=datetime.utcnow)
    note: Mapped[int] = mapped_column()
    comment: Mapped[str] = mapped_column()

    def __repr__(self) -> str:
        return f"<Survey id={self.id}>"
