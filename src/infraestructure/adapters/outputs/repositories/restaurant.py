from sqlalchemy import func, select
from sqlalchemy import update as sql_update
from sqlalchemy.orm import Session, joinedload

from src.domain.entities.restaurant import (
    RestaurantBase,
    RestaurantBaseInput,
    RestaurantWithRelations,
)
from src.domain.repositories.restaurant import IRestaurantRepository
from src.infraestructure.adapters.outputs.db.models import (
    CategoryModel,
    RestaurantModel,
)


class RestaurantRepository(IRestaurantRepository):
    def __init__(self, session: Session):
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
    ) -> list[RestaurantBase]:
        query = select(RestaurantModel)
        if filters and filters.get("id"):
            query = query.where(RestaurantModel.id == filters.get("id"))
        if filters and filters.get("name"):
            query = query.where(RestaurantModel.name.ilike(f'%{filters.get("name")}%'))
        if filters and filters.get("address"):
            query = query.where(
                RestaurantModel.address.ilike(f'%{filters.get("address")}%')
            )
        if filters and filters.get("rating_lte"):
            query = query.where(RestaurantModel.rating <= filters.get("rating_lte"))
        if filters and filters.get("rating_gte"):
            query = query.where(RestaurantModel.rating >= filters.get("rating_gte"))
        if filters and filters.get("is_active"):
            query = query.where(RestaurantModel.is_active == filters.get("is_active"))
        if page:
            query = query.offset((page * size) - size)
        if size:
            query = query.limit(size)
        result = await self.session.execute(query)
        restaurants = result.scalars().all()
        return [
            RestaurantBase.model_validate(restaurant, from_attributes=True)
            for restaurant in restaurants
        ]

    async def get_by_id(self, restaurant_id: int) -> RestaurantWithRelations | None:
        query = select(RestaurantModel).where(RestaurantModel.id == restaurant_id)
        result = await self.session.execute(query)
        restaurant = result.scalars().first()
        return (
            RestaurantWithRelations.model_validate(restaurant, from_attributes=True)
            if restaurant
            else None
        )

    async def create(self, restaurant: RestaurantBaseInput) -> RestaurantWithRelations:
        restaurant_model = RestaurantModel(**restaurant.model_dump())
        self.session.add(restaurant_model)
        await self.session.commit()
        restaurant_model = await self.get_by_id(restaurant_model.id)
        return RestaurantWithRelations.model_validate(
            restaurant_model, from_attributes=True
        )

    async def update(
        self, restaurant_id: int, restaurant: RestaurantBaseInput
    ) -> RestaurantWithRelations:
        execute_update = (
            sql_update(RestaurantModel)
            .where(RestaurantModel.id == restaurant_id)
            .values(**restaurant.model_dump())
            .execution_options(synchronize_session="fetch")
        )
        await self.session.execute(execute_update)
        await self.session.commit()
        restaurant_model = await self.get_by_id(restaurant_id)
        return RestaurantWithRelations.model_validate(
            restaurant_model, from_attributes=True
        )

    async def deactivate(self, restaurant_id: int) -> RestaurantWithRelations:
        execute_update = (
            sql_update(RestaurantModel)
            .where(RestaurantModel.id == restaurant_id)
            .values(is_active=False)
            .execution_options(synchronize_session="fetch")
        )
        await self.session.execute(execute_update)
        await self.session.commit()
        restaurant_model = await self.get_by_id(restaurant_id)
        return RestaurantWithRelations.model_validate(
            restaurant_model, from_attributes=True
        )
