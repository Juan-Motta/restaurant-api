from src.domain.entities.pagination import Page, paginate
from src.domain.entities.rating import RatingBase, RatingBaseInput, RatingWithRelations
from src.domain.repositories.rating import IRatingRepository


class RatingService:
    def __init__(self, rating_repository: IRatingRepository):
        self.rating_repository = rating_repository

    async def get_all(
        self, page: int = 1, size: int = 10, filters: dict | None = None
    ) -> Page[RatingBase]:
        all_ratings_count = await self.rating_repository.count_all()
        ratings = await self.rating_repository.get_all(
            page=page, size=size, filters=filters
        )
        return paginate(data=ratings, page=page, size=size, total=all_ratings_count)

    async def get_by_id(self, rating_id: int) -> RatingWithRelations:
        return await self.rating_repository.get_by_id(rating_id)

    async def create(self, data: RatingBaseInput) -> RatingWithRelations:
        return await self.rating_repository.create(data)

    async def update(
        self, rating_id: int, data: RatingBaseInput
    ) -> RatingWithRelations:
        return await self.rating_repository.update(rating_id, data)

    async def deactivate(self, rating_id: int) -> RatingWithRelations:
        return await self.rating_repository.deactivate(rating_id)
