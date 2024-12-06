import random
from decimal import Decimal

import factory.fuzzy

from src.infraestructure.adapters.outputs.db.models import OrderItemModel
from tests.factories.base_factory import BaseFactory


class OrderItemFactory(BaseFactory):
    class Meta:
        model = OrderItemModel

    order = factory.SubFactory("tests.factories.order_factory.OrderFactory")
    menu_item = factory.SubFactory("tests.factories.menu_item_factory.MenuItemFactory")
    quantity = factory.Faker("random_number", digits=1)
    sub_total = factory.Faker("pydecimal", left_digits=4, right_digits=2, positive=True)
    total = factory.Faker("pydecimal", left_digits=4, right_digits=2, positive=True)
    notes = factory.Faker("text")
