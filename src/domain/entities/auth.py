from typing import Union

from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator


class AuthUserBase(BaseModel):
    id: int
    first_name: str
    last_name: str
    email: str
    phone: str
    address: str
    restaurant_id: int
    access_token: str | None = None

    model_config = ConfigDict(from_attributes=True)


class AuthCreatePasswordInput(BaseModel):
    username: int | str = Field(..., union_mode="left_to_right")
    password_1: str = Field(..., min_length=3, max_length=255)
    password_2: str = Field(..., min_length=3, max_length=255)

    @model_validator(mode="after")
    def validate_passwords(self):
        if self.password_1 != self.password_2:
            raise ValueError("Passwords do not match")
        return self


class AuthLoginInput(BaseModel):
    username: int | str = Field(..., union_mode="left_to_right")
    password: str = Field(..., min_length=3, max_length=255)
