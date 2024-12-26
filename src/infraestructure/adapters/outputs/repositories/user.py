from sqlalchemy import func, select
from sqlalchemy import update as sql_update
from sqlalchemy.orm import Session

from src.domain.entities.user import UserBase, UserBaseInput, UserWithRelations
from src.domain.repositories.user import IUserRepository
from src.infraestructure.adapters.outputs.db.models import (
    UserModel,
)


class UserRepository(IUserRepository):
    def __init__(self, session: Session):
        self.session = session

    async def count_all(self, filters: dict | None = None):
        query = (
            select(func.count())
            .select_from(UserModel)
            .where(UserModel.is_active == True)
        )
        if filters and filters.get("id"):
            query = query.where(UserModel.id == filters.get("id"))
        if filters and filters.get("first_name"):
            query = query.where(UserModel.name.ilike(f'%{filters.get("first_name")}%'))
        if filters and filters.get("last_name"):
            query = query.where(UserModel.name.ilike(f'%{filters.get("last_name")}%'))
        if filters and filters.get("email"):
            query = query.where(UserModel.email.ilike(f'%{filters.get("email")}%'))
        if filters and filters.get("phone"):
            query = query.where(UserModel.phone.ilike(f'%{filters.get("phone")}%'))
        if filters and filters.get("address"):
            query = query.where(UserModel.address.ilike(f'%{filters.get("address")}%'))
        if filters and filters.get("restaurant_id"):
            query = query.where(UserModel.restaurant_id == filters.get("restaurant_id"))
        if filters and filters.get("is_active") in (True, False):
            query = query.where(UserModel.is_active == filters.get("is_active"))
        result = await self.session.execute(query)
        return result.scalar()

    async def get_all(
        self,
        page: int | None = None,
        size: int | None = None,
        filters: dict | None = None,
    ) -> list[UserBase]:
        query = select(UserModel)
        if filters and filters.get("id"):
            query = query.where(UserModel.id == filters.get("id"))
        if filters and filters.get("first_name"):
            query = query.where(UserModel.name.ilike(f'%{filters.get("first_name")}%'))
        if filters and filters.get("last_name"):
            query = query.where(UserModel.name.ilike(f'%{filters.get("last_name")}%'))
        if filters and filters.get("email"):
            query = query.where(UserModel.email.ilike(f'%{filters.get("email")}%'))
        if filters and filters.get("phone"):
            query = query.where(UserModel.phone.ilike(f'%{filters.get("phone")}%'))
        if filters and filters.get("address"):
            query = query.where(UserModel.address.ilike(f'%{filters.get("address")}%'))
        if filters and filters.get("restaurant_id"):
            query = query.where(UserModel.restaurant_id == filters.get("restaurant_id"))
        if filters and filters.get("is_active") in (True, False):
            query = query.where(UserModel.is_active == filters.get("is_active"))
        if page:
            query = query.offset((page * size) - size)
        if size:
            query = query.limit(size)
        result = await self.session.execute(query)
        users = result.scalars().all()
        return [UserBase.model_validate(user, from_attributes=True) for user in users]

    async def get_by_id(self, user_id: int) -> UserWithRelations | None:
        query = select(UserModel).where(UserModel.id == user_id)
        result = await self.session.execute(query)
        user = result.scalars().first()
        return (
            UserWithRelations.model_validate(user, from_attributes=True)
            if user
            else None
        )

    async def get_by_email(self, email: str) -> UserWithRelations | None:
        query = select(UserModel).where(UserModel.email == email)
        result = await self.session.execute(query)
        user = result.scalars().first()
        return (
            UserWithRelations.model_validate(user, from_attributes=True)
            if user
            else None
        )

    async def get_password(self, user_id: int) -> str | None:
        query = select(UserModel.password).where(UserModel.id == user_id)
        result = await self.session.execute(query)
        password = result.scalar()
        return password

    async def create(self, user: UserBaseInput) -> UserWithRelations:
        user_model = UserModel(**user.model_dump(), is_active=False)
        self.session.add(user_model)
        await self.session.commit()
        user_model = await self.get_by_id(user_model.id)
        return UserWithRelations.model_validate(user_model, from_attributes=True)

    async def update(self, user_id: int, user: UserBaseInput) -> UserWithRelations:
        execute_update = (
            sql_update(UserModel)
            .where(UserModel.id == user_id)
            .values(**user.model_dump())
            .execution_options(synchronize_session="fetch")
        )
        await self.session.execute(execute_update)
        await self.session.commit()
        user_model = await self.get_by_id(user_id)
        return UserWithRelations.model_validate(user_model, from_attributes=True)

    async def deactivate(self, user_id: int) -> UserWithRelations:
        execute_update = (
            sql_update(UserModel)
            .where(UserModel.id == user_id)
            .values(is_active=False)
            .execution_options(synchronize_session="fetch")
        )
        await self.session.execute(execute_update)
        await self.session.commit()
        user_model = await self.get_by_id(user_id)
        return UserWithRelations.model_validate(user_model, from_attributes=True)

    async def update_password(self, user_id: int, password: str) -> UserWithRelations:
        execute_update = (
            sql_update(UserModel)
            .where(UserModel.id == user_id)
            .values(password=password, is_active=True)
            .execution_options(synchronize_session="fetch")
        )
        await self.session.execute(execute_update)
        await self.session.commit()
        user_model = await self.get_by_id(user_id)
        return UserWithRelations.model_validate(user_model, from_attributes=True)
