import binascii
import hashlib
from typing import TYPE_CHECKING, List

from sqlalchemy import ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.config.settings import settings
from app.database.base import Base
from app.database.mixins import TimestampMixin

if TYPE_CHECKING:
    from app.models import Order, Payment, Profile, Store


class User(Base, TimestampMixin):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    first_name: Mapped[str] = mapped_column(index=True)
    last_name: Mapped[str] = mapped_column(index=True)
    email: Mapped[str] = mapped_column(index=True, unique=True)
    nid: Mapped[str] = mapped_column(index=True)
    password: Mapped[str] = mapped_column(index=True)

    profiles: Mapped[List["UserProfile"]] = relationship(back_populates="user")
    stores: Mapped[List["UserStore"]] = relationship(back_populates="user")
    orders: Mapped[List["Order"]] = relationship(back_populates="user")
    payments: Mapped[List["Payment"]] = relationship(back_populates="user")

    def set_password(self, password: str) -> None:
        dk = hashlib.pbkdf2_hmac(
            "sha256",
            password.encode("utf-8"),
            settings.SECRET_KEY.encode("utf-8"),
            100000,
        )
        hashed_password = binascii.hexlify(dk).decode("utf-8")
        self.password = f"pbkdf2_sha256$100000${hashed_password}"

    def check_password(self, password: str) -> bool:
        dk = hashlib.pbkdf2_hmac(
            "sha256",
            password.encode("utf-8"),
            settings.SECRET_KEY.encode("utf-8"),
            100000,
        )
        hashed_password = binascii.hexlify(dk).decode("utf-8")
        return self.password == f"pbkdf2_sha256$100000${hashed_password}"

    def __repr__(self) -> str:
        return f"<User id={self.id} email={self.email} active={self.active}>"


class UserProfile(Base, TimestampMixin):
    __tablename__ = "user_profiles"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)

    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    user: Mapped["User"] = relationship(back_populates="profiles")

    profile_id: Mapped[int] = mapped_column(ForeignKey("profiles.id"))
    profile: Mapped[List["Profile"]] = relationship(back_populates="users")

    __table_args__ = (
        UniqueConstraint(
            'user_id', 'profile_id', name='_unique_user_id_profile'
        ),
    )

    def __repr__(self) -> str:
        return f"<UserProfile id={self.id} user_id={self.user_id} profile_id={self.profile_id}>"


class UserStore(Base, TimestampMixin):
    __tablename__ = "user_stores"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)

    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    user: Mapped["User"] = relationship(back_populates="stores")

    store_id: Mapped[int] = mapped_column(ForeignKey("stores.id"))
    store: Mapped["Store"] = relationship(back_populates="users")

    __table_args__ = (
        UniqueConstraint(
            'user_id', 'store_id', name='_unique_user_id_store_id'
        ),
    )

    def __repr__(self) -> str:
        return f"<UserStore id={self.id} user_id={self.user_id} store_id={self.store_id}>"
