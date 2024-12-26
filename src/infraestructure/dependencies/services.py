from sqlalchemy.orm import Session

from src.application.services.auth import AuthService
from src.application.services.menu_item import MenuItemService
from src.application.services.order import OrderService
from src.application.services.order_item import OrderItemService
from src.application.services.permission import PermissionService
from src.application.services.rating import RatingService
from src.application.services.restaurant import RestaurantService
from src.application.services.user import UserService
from src.infraestructure.dependencies.repositories import (
    get_menu_item_repository,
    get_order_item_repository,
    get_order_repository,
    get_permission_repository,
    get_rating_repository,
    get_restaurant_repository,
    get_user_repository,
)
from src.infraestructure.utils.jwt import JWTManager
from src.infraestructure.utils.password import PasswordManager


def get_restaurant_service(session: Session) -> RestaurantService:
    restaurant_repository = get_restaurant_repository(session=session)
    restaurant_service = RestaurantService(restaurant_repository=restaurant_repository)
    return restaurant_service


def get_user_service(session: Session) -> UserService:
    user_repository = get_user_repository(session=session)
    user_service = UserService(user_repository=user_repository)
    return user_service


def get_menu_item_service(session: Session) -> MenuItemService:
    menu_item_repository = get_menu_item_repository(session=session)
    menu_item_service = MenuItemService(menu_item_repository=menu_item_repository)
    return menu_item_service


def get_order_service(session: Session) -> OrderService:
    order_repository = get_order_repository(session=session)
    order_service = OrderService(order_repository=order_repository)
    return order_service


def get_order_item_service(session: Session) -> OrderItemService:
    order_item_repository = get_order_item_repository(session=session)
    order_item_service = OrderItemService(order_item_repository=order_item_repository)
    return order_item_service


def get_rating_service(session: Session) -> RatingService:
    rating_repository = get_rating_repository(session=session)
    rating_service = RatingService(rating_repository=rating_repository)
    return rating_service


def get_auth_service(session: Session) -> AuthService:
    user_repository = get_user_repository(session=session)
    permission_repository = get_permission_repository(session=session)
    password_manager = PasswordManager
    jwt_manager = JWTManager
    auth_service = AuthService(
        user_repository=user_repository,
        permission_repository=permission_repository,
        password_manager=password_manager,
        jwt_manager=jwt_manager,
    )
    return auth_service


def get_permission_service(session: Session) -> PermissionService:
    permission_repository = get_permission_repository(session=session)
    permission_service = PermissionService(permission_repository=permission_repository)
    return permission_service
