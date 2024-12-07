from src.application.commons.pagination import paginate
from src.domain.entities.pagination import Page
from src.domain.entities.restaurant import (
    RestaurantBase,
    RestaurantBaseInput,
    RestaurantWithRelations,
)
from src.domain.repositories.restaurant import IRestaurantRepository


class RestaurantService:
    def __init__(self, restaurant_repository: IRestaurantRepository):
        self.restaurant_repository = restaurant_repository

    async def get_all(
        self, page: int = 1, size: int = 10, filters: dict | None = None
    ) -> Page[RestaurantBase]:
        all_restaurants_count = await self.restaurant_repository.count_all()
        restaurants = await self.restaurant_repository.get_all(
            page=page, size=size, filters=filters
        )
        return paginate(
            data=restaurants, page=page, size=size, total=all_restaurants_count
        )

    async def get_by_id(self, restaurant_id: int) -> RestaurantWithRelations:
        return await self.restaurant_repository.get_by_id(restaurant_id)

    async def create(self, data: RestaurantBaseInput) -> RestaurantWithRelations:
        return await self.restaurant_repository.create(data)

    async def update(
        self, restaurant_id: int, data: RestaurantBaseInput
    ) -> RestaurantWithRelations:
        return await self.restaurant_repository.update(restaurant_id, data)

    async def deactivate(self, restaurant_id: int) -> RestaurantWithRelations:
        return await self.restaurant_repository.deactivate(restaurant_id)
