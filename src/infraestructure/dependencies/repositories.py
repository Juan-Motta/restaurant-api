from sqlalchemy.orm import Session

from src.infraestructure.adapters.outputs.repositories.restaurant import (
    RestaurantRepository,
)
from src.infraestructure.adapters.outputs.repositories.user import UserRepository


def get_restaurant_repository(session: Session) -> RestaurantRepository:
    return RestaurantRepository(session=session)


def get_user_repository(session: Session) -> UserRepository:
    return UserRepository(session=session)
