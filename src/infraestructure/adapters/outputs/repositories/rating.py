from sqlalchemy import func, select
from sqlalchemy import update as sql_update
from sqlalchemy.orm import Session, joinedload

from src.domain.entities.rating import RatingBase, RatingBaseInput, RatingWithRelations
from src.domain.repositories.rating import IRatingRepository
from src.infraestructure.adapters.outputs.db.models import OrderModel, RatingModel


class RatingRepository(IRatingRepository):
    def __init__(self, session: Session):
        self.session = session

    async def count_all(self):
        query = (
            select(func.count())
            .select_from(RatingModel)
            .where(RatingModel.is_active == True)
        )
        result = await self.session.execute(query)
        return result.scalar()

    async def get_all(
        self,
        page: int | None = None,
        size: int | None = None,
        filters: dict | None = None,
    ) -> list[RatingBase]:
        query = select(RatingModel)
        if filters and filters.get("id"):
            query = query.where(RatingModel.id == filters.get("id"))
        if filters and filters.get("rating_lte"):
            query = query.where(RatingModel.rating <= filters.get("rating_lte"))
        if filters and filters.get("rating_gte"):
            query = query.where(RatingModel.rating >= filters.get("rating_gte"))
        if filters and filters.get("comment"):
            query = query.where(
                RatingModel.comment.ilike(f"""%{filters.get("comment")}%""")
            )
        if filters and filters.get("order_id"):
            query = query.where(RatingModel.order_id == filters.get("order_id"))
        if filters and filters.get("is_active") in (True, False):
            query = query.where(RatingModel.is_active == filters.get("is_active"))
        if page:
            query = query.offset((page * size) - size)
        if size:
            query = query.limit(size)
        result = await self.session.execute(query)
        ratings = result.scalars().all()
        return [
            RatingBase.model_validate(rating, from_attributes=True)
            for rating in ratings
        ]

    async def get_by_id(self, rating_id: int) -> RatingWithRelations | None:
        query = select(RatingModel).where(RatingModel.id == rating_id)
        result = await self.session.execute(query)
        rating = result.scalars().first()
        return (
            RatingWithRelations.model_validate(rating, from_attributes=True)
            if rating
            else None
        )

    async def create(self, rating: RatingBaseInput) -> RatingWithRelations:
        rating_model = RatingModel(**rating.model_dump())
        self.session.add(rating_model)
        await self.session.commit()
        rating_model = await self.get_by_id(rating_model.id)
        return RatingWithRelations.model_validate(rating_model, from_attributes=True)

    async def update(
        self, rating_id: int, rating: RatingBaseInput
    ) -> RatingWithRelations:
        execute_update = (
            sql_update(RatingModel)
            .where(RatingModel.id == rating_id)
            .values(**rating.model_dump())
            .execution_options(synchronize_session="fetch")
        )
        await self.session.execute(execute_update)
        await self.session.commit()
        rating_model = await self.get_by_id(rating_id)
        return RatingWithRelations.model_validate(rating_model, from_attributes=True)

    async def deactivate(self, rating_id: int) -> RatingWithRelations:
        execute_update = (
            sql_update(RatingModel)
            .where(RatingModel.id == rating_id)
            .values(is_active=False)
            .execution_options(synchronize_session="fetch")
        )
        await self.session.execute(execute_update)
        await self.session.commit()
        rating_model = await self.get_by_id(rating_id)
        return RatingWithRelations.model_validate(rating_model, from_attributes=True)
