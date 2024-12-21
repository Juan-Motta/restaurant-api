from src.domain.entities.user import UserBase, UserBaseInput, UserWithRelations


class IUserRepository:
    async def count_all(self) -> int:
        raise NotImplementedError

    async def get_all(
        self,
        page: int | None = None,
        size: int | None = None,
        filters: dict | None = None,
    ) -> list[UserBase]:
        raise NotImplementedError

    async def get_by_id(self, user_id: int) -> UserWithRelations | None:
        raise NotImplementedError

    async def get_by_email(self, email: str) -> UserWithRelations | None:
        raise NotImplementedError

    async def get_password(self, user_id: int) -> str | None:
        raise NotImplementedError

    async def create(self, data: UserBaseInput) -> UserWithRelations:
        raise NotImplementedError

    async def update(self, user_id: int, data: UserBaseInput) -> UserWithRelations:
        raise NotImplementedError

    async def deactivate(self, user_id: int) -> UserWithRelations:
        raise NotImplementedError

    async def update_password(self, user_id: int, password: str) -> UserWithRelations:
        raise NotImplementedError
