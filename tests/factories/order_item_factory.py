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
    sub_total = round(Decimal(random.uniform(1, 100000)), 2)
    total = round(Decimal(random.uniform(1, 100000)), 2)
    notes = factory.Faker("text")
