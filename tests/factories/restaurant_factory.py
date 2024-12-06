import random
from decimal import Decimal

import factory.fuzzy

from src.infraestructure.adapters.outputs.db.models import (
    RestaurantModel,
    RestaurantStatusEnum,
)
from tests.factories.base_factory import BaseFactory


class RestaurantFactory(BaseFactory):
    class Meta:
        model = RestaurantModel

    name = factory.Faker("company")
    address = factory.Faker("address")
    rating = round(Decimal(random.uniform(1, 5)), 2)
    status = factory.fuzzy.FuzzyChoice(
        choices=[status for status in RestaurantStatusEnum]
    )
    latitude = factory.Faker("latitude")
    longitude = factory.Faker("longitude")
    category = factory.SubFactory("tests.factories.category_factory.CategoryFactory")
