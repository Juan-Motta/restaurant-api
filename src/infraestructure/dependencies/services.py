from sqlalchemy.orm import Session

from src.application.services.menu_item import MenuItemService
from src.application.services.restaurant import RestaurantService
from src.application.services.user import UserService
from src.infraestructure.dependencies.repositories import (
    get_menu_item_repository,
    get_restaurant_repository,
    get_user_repository,
)


def get_restaurant_service(session: Session) -> RestaurantService:
    restaurant_repository = get_restaurant_repository(session=session)
    restaurant_service = RestaurantService(restaurant_repository=restaurant_repository)
    return restaurant_service


def get_user_service(session: Session) -> UserService:
    user_repository = get_user_repository(session=session)
    user_service = UserService(user_repository=user_repository)
    return user_service


def get_menu_item_service(session: Session) -> UserService:
    menu_item_repository = get_menu_item_repository(session=session)
    menu_item_service = MenuItemService(menu_item_repository=menu_item_repository)
    return menu_item_service
