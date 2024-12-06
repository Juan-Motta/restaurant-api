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
    rating = factory.Faker("pydecimal", left_digits=2, right_digits=2, positive=True)
    status = factory.fuzzy.FuzzyChoice(
        choices=[status for status in RestaurantStatusEnum]
    )
    latitude = factory.Faker("latitude")
    longitude = factory.Faker("longitude")
    category = factory.SubFactory("tests.factories.category_factory.CategoryFactory")
