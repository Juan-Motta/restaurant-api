import factory.fuzzy

from src.infraestructure.adapters.outputs.db.models import (
    CategoryModel,
    CategoryTypologyEnum,
)
from tests.factories.base_factory import BaseFactory


class CategoryFactory(BaseFactory):
    class Meta:
        model = CategoryModel

    name = factory.Faker("word")
    description = factory.Faker("text")
    typology = factory.fuzzy.FuzzyChoice(
        choices=[category_type for category_type in CategoryTypologyEnum]
    )
