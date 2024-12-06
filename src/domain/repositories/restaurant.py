from src.domain.entities.restaurant import Restaurant


class IRestaurantRepository:
    async def get_all(self) -> list[Restaurant]:
        raise NotImplementedError
