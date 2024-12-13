from src.domain.entities.rating import RatingBase, RatingBaseInput, RatingWithRelations


class IRatingRepository:
    async def count_all(self) -> int:
        raise NotImplementedError

    async def get_all(
        self,
        page: int | None = None,
        size: int | None = None,
        filters: dict | None = None,
    ) -> list[RatingBase]:
        raise NotImplementedError

    async def get_by_id(self, rating_id: int) -> RatingWithRelations | None:
        raise NotImplementedError

    async def create(self, data: RatingBaseInput) -> RatingWithRelations:
        raise NotImplementedError

    async def update(
        self, rating_id: int, data: RatingBaseInput
    ) -> RatingWithRelations:
        raise NotImplementedError

    async def deactivate(self, rating_id: int) -> RatingWithRelations:
        raise NotImplementedError
