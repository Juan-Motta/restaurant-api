from decimal import Decimal

from pydantic import BaseModel, ConfigDict


class Restaurant(BaseModel):
    id: int
    name: str
    address: str
    rating: Decimal
    status: str
    latitude: Decimal
    longitude: Decimal

    class Config:
        model_config = ConfigDict(from_attributes=True)
