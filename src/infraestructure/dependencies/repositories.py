from sqlalchemy.orm import Session

from src.infraestructure.adapters.outputs.repositories.menu_item import (
    MenuItemRepository,
)
from src.infraestructure.adapters.outputs.repositories.order import OrderRepository
from src.infraestructure.adapters.outputs.repositories.order_item import (
    OrderItemRepository,
)
from src.infraestructure.adapters.outputs.repositories.rating import RatingRepository
from src.infraestructure.adapters.outputs.repositories.restaurant import (
    RestaurantRepository,
)
from src.infraestructure.adapters.outputs.repositories.user import UserRepository


def get_restaurant_repository(session: Session) -> RestaurantRepository:
    return RestaurantRepository(session=session)


def get_user_repository(session: Session) -> UserRepository:
    return UserRepository(session=session)


def get_menu_item_repository(session: Session) -> MenuItemRepository:
    return MenuItemRepository(session=session)


def get_order_repository(session: Session) -> OrderRepository:
    return OrderRepository(session=session)


def get_order_item_repository(session: Session) -> OrderItemRepository:
    return OrderItemRepository(session=session)


def get_rating_repository(session: Session) -> RatingRepository:
    return RatingRepository(session=session)
