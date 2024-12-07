from src.domain.entities.restaurant import (
    RestaurantBase,
    RestaurantBaseInput,
    RestaurantWithRelations,
)


class IRestaurantRepository:
    async def count_all(self) -> int:
        raise NotImplementedError

    async def get_all(
        self,
        page: int | None = None,
        size: int | None = None,
        filters: dict | None = None,
    ) -> list[RestaurantBase]:
        raise NotImplementedError

    async def get_by_id(self, restaurant_id: int) -> RestaurantWithRelations | None:
        raise NotImplementedError

    async def create(self, data: RestaurantBaseInput) -> RestaurantWithRelations:
        raise NotImplementedError
