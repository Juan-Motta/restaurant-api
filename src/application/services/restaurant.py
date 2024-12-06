from src.application.commons.pagination import paginate
from src.domain.entities.pagination import Page
from src.domain.entities.restaurant import Restaurant
from src.domain.repositories.restaurant import IRestaurantRepository


class RestaurantService:
    def __init__(self, restaurant_repository: IRestaurantRepository):
        self.restaurant_repository = restaurant_repository

    async def get_all(
        self, page: int = 1, size: int = 10, filters: dict | None = None
    ) -> Page[Restaurant]:
        all_restaurants_count = await self.restaurant_repository.count_all()
        restaurants = await self.restaurant_repository.get_all(
            page=page, size=size, filters=filters
        )
        return paginate(
            data=restaurants, page=page, size=size, total=all_restaurants_count
        )
