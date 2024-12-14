from fastapi import Query
from pydantic import BaseModel


class UserFilter(BaseModel):
    id: int | None = Query(None, description="User ID", ge=1)
    first_name: str | None = Query(
        None, description="User first name", min_length=1, max_length=100
    )
    last_name: str | None = Query(
        None, description="User last name", min_length=1, max_length=100
    )
    email: str | None = Query(
        None, description="User email", min_length=1, max_length=255
    )
    phone: str | None = Query(
        None, description="User phone", min_length=1, max_length=20
    )
    address: str | None = Query(
        None, description="User address", min_length=1, max_length=255
    )
    restaurant_id: int | None = Query(None, description="Restaurant ID", ge=1)
    is_active: bool = Query(True, description="User active status")
