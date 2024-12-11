import re

from pydantic import BaseModel, ConfigDict, Field, field_validator

from src.domain.entities.restaurant import RestaurantBase


class UserBase(BaseModel):
    id: int
    first_name: str
    last_name: str
    email: str
    phone: str
    address: str
    is_active: bool

    model_config = ConfigDict(from_attributes=True)


class UserWithRelations(BaseModel):
    id: int
    first_name: str
    last_name: str
    email: str
    phone: str
    address: str
    restaurant: RestaurantBase
    # orders: list[OrderBase]

    model_config = ConfigDict(from_attributes=True)


class UserBaseInput(BaseModel):
    first_name: str = Field(..., min_length=3, max_length=100)
    last_name: str = Field(..., min_length=3, max_length=100)
    email: str = Field(..., min_length=3, max_length=255)
    phone: str = Field(..., min_length=3, max_length=20)
    address: str = Field(..., min_length=3, max_length=255)
    restaurant_id: int = Field(..., ge=1)

    @field_validator("first_name", "last_name")
    @classmethod
    def validate_name(cls, v):
        if not v:
            raise ValueError("Name must not be empty")
        elif not v.isalpha():
            raise ValueError("Name must be alphabetic")
        return v.lower()

    @field_validator("email")
    @classmethod
    def validate_email(cls, v):
        if not v:
            raise ValueError("Email must not be empty")
        return v.lower()

    @field_validator("phone")
    @classmethod
    def validate_phone(cls, v):
        if not v:
            raise ValueError("Phone must not be empty")
        return v

    @field_validator("address")
    @classmethod
    def validate_address(cls, v):
        if not v:
            raise ValueError("Address must not be empty")
        return v.lower()