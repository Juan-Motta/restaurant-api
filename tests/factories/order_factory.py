import random
from decimal import Decimal

import factory.fuzzy

from src.infraestructure.adapters.outputs.db.models import OrderModel, OrderStatusEnum
from tests.factories.base_factory import BaseFactory


class OrderFactory(BaseFactory):
    class Meta:
        model = OrderModel

    status = factory.fuzzy.FuzzyChoice(choices=[status for status in OrderStatusEnum])
    total_amount = factory.Faker(
        "pydecimal", left_digits=4, right_digits=2, positive=True
    )
    delivery_address = factory.Faker("address")
    special_instructions = factory.Faker("text")
    estimated_delivery_time = factory.Faker("date_time")
    restaurant = factory.SubFactory(
        "tests.factories.restaurant_factory.RestaurantFactory"
    )
    customer = factory.SubFactory("tests.factories.user_factory.UserFactory")
