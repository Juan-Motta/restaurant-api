import random
from decimal import Decimal

import factory.fuzzy

from src.infraestructure.adapters.outputs.db.models import RatingModel
from tests.factories.base_factory import BaseFactory


class RatingFactory(BaseFactory):
    class Meta:
        model = RatingModel

    order = factory.SubFactory("tests.factories.order_factory.OrderFactory")
    rating = factory.Faker("pydecimal", left_digits=2, right_digits=2, positive=True)
    comment = factory.Faker("text")
