from src.domain.entities.restaurant import Restaurant
from src.domain.repositories.restaurant import IRestaurantRepository


class RestaurantService:
    def __init__(self, repository: IRestaurantRepository):
        self.repository = repository

    async def get_all(self) -> list[Restaurant]:
        return await self.repository.get_all()
