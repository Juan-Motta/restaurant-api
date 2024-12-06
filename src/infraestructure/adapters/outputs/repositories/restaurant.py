from sqlalchemy import func, select

from src.domain.entities.restaurant import Restaurant
from src.domain.repositories.restaurant import IRestaurantRepository
from src.infraestructure.adapters.outputs.db.models import RestaurantModel


class RestaurantRepository(IRestaurantRepository):
    def __init__(self, session):
        self.session = session

    async def count_all(self):
        query = select(func.count()).select_from(RestaurantModel)
        result = await self.session.execute(query)
        return result.scalar()

    async def get_all(
        self,
        page: int | None = None,
        size: int | None = None,
        filters: dict | None = None,
    ):
        query = select(RestaurantModel)
        if size:
            query = query.limit(size)
        if page:
            query = query.offset(page * size)
        if filters and filters.get("id"):
            query = query.where(RestaurantModel.id == filters.get("id"))
        if filters and filters.get("name"):
            query = query.where(RestaurantModel.name.ilike(filters.get("name")))
        result = await self.session.execute(query)
        restaurants = result.scalars().all()
        return [
            Restaurant.model_validate(restaurant.__dict__, from_attributes=True)
            for restaurant in restaurants
        ]
