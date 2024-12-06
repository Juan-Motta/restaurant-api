import random
from decimal import Decimal

import factory.fuzzy

from src.infraestructure.adapters.outputs.db.models import RatingModel
from tests.factories.base_factory import BaseFactory


class RatingFactory(BaseFactory):
    class Meta:
        model = RatingModel

    order = factory.SubFactory("tests.factories.order_factory.OrderFactory")
    rating = round(Decimal(random.uniform(1, 10)), 2)
    comment = factory.Faker("text")
