from sqlalchemy.orm import Session

from src.application.services.restaurant import RestaurantService
from src.infraestructure.dependencies.repositories import get_restaurant_repository


def get_restaurant_service(session: Session) -> RestaurantService:
    restaurant_repository = get_restaurant_repository(session=session)
    restaurant_service = RestaurantService(restaurant_repository=restaurant_repository)
    return restaurant_service
