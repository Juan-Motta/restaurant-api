from sqlalchemy.orm import Session

from src.infraestructure.adapters.outputs.repositories.restaurant import (
    RestaurantRepository,
)


def get_restaurant_repository(session: Session) -> RestaurantRepository:
    return RestaurantRepository(session=session)
