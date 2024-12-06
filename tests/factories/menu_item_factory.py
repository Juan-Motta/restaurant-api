import random
from decimal import Decimal

import factory.fuzzy

from src.infraestructure.adapters.outputs.db.models import MenuItemModel
from tests.factories.base_factory import BaseFactory


class MenuItemFactory(BaseFactory):
    class Meta:
        model = MenuItemModel

    name = factory.Faker("word")
    description = factory.Faker("text")
    price = factory.Faker("pydecimal", left_digits=4, right_digits=2, positive=True)
    preparation_time = factory.Faker("random_number", digits=4)
    available = factory.Faker("boolean")
    image_url = factory.Faker("image_url")
    category = factory.SubFactory("tests.factories.category_factory.CategoryFactory")
    restaurant = factory.SubFactory(
        "tests.factories.restaurant_factory.RestaurantFactory"
    )
