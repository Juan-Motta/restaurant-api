import random
from decimal import Decimal

import factory.fuzzy

from src.infraestructure.adapters.outputs.db.models import UserModel, UserTypologyEnum
from tests.factories.base_factory import BaseFactory


class UserFactory(BaseFactory):
    class Meta:
        model = UserModel

    typology = factory.fuzzy.FuzzyChoice(
        choices=[typology for typology in UserTypologyEnum]
    )
    first_name = factory.Faker("name")
    last_name = factory.Faker("name")
    email = factory.Faker("email")
    phone = factory.Faker("random_number", digits=10)
    address = factory.Faker("address")
    restaurant = factory.SubFactory(
        "tests.factories.restaurant_factory.RestaurantFactory"
    )
