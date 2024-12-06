from faker import Faker

from tests.factories.menu_item_factory import MenuItemFactory
from tests.factories.order_factory import OrderFactory
from tests.factories.order_item_factory import OrderItemFactory
from tests.factories.rating_factory import RatingFactory
from tests.factories.restaurant_factory import RestaurantFactory
from tests.factories.user_factory import UserFactory

faker = Faker()


def generate_data():
    RestaurantFactory()
    UserFactory()
    OrderFactory()
    RatingFactory()
    MenuItemFactory()
    for _ in range(2):
        OrderItemFactory()


if __name__ == "__main__":
    generate_data()
