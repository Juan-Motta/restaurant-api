from datetime import datetime

from sqlalchemy import DateTime, func
from sqlalchemy.orm import Mapped, mapped_column


class IntegerIdMixin:
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)


class UUIDIdMixin:
    id: Mapped[str] = mapped_column(primary_key=True, default=func.uuid_generate_v4())


class TimestampMixin:
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )


class IsActiveMixin:
    is_active: Mapped[bool] = mapped_column(default=True)
