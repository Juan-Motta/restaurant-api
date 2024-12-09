from src.domain.entities.pagination import Page, paginate
from src.domain.entities.user import UserBase, UserBaseInput, UserWithRelations
from src.domain.repositories.user import IUserRepository


class UserService:
    def __init__(self, user_repository: IUserRepository):
        self.user_repository = user_repository

    async def get_all(
        self, page: int = 1, size: int = 10, filters: dict | None = None
    ) -> Page[UserBase]:
        all_users_count = await self.user_repository.count_all()
        users = await self.user_repository.get_all(
            page=page, size=size, filters=filters
        )
        return paginate(data=users, page=page, size=size, total=all_users_count)

    async def get_by_id(self, user_id: int) -> UserWithRelations:
        return await self.user_repository.get_by_id(user_id)

    async def create(self, data: UserBaseInput) -> UserWithRelations:
        return await self.user_repository.create(data)

    async def update(self, user_id: int, data: UserBaseInput) -> UserWithRelations:
        return await self.user_repository.update(user_id, data)

    async def deactivate(self, user_id: int) -> UserWithRelations:
        return await self.user_repository.deactivate(user_id)
