from sqlalchemy import select
from sqlalchemy.orm import Session

from src.domain.entities.permission import PermissionBase
from src.domain.repositories.permission import IPermissionRepository
from src.infraestructure.adapters.outputs.db.models import (
    PermissionModel,
    RoleModel,
    RolePermissionModel,
    UserPermissionModel,
)


class PermissionRepository(IPermissionRepository):
    def __init__(self, session: Session):
        self.session = session

    async def get_all_by_role_id(self, role_id: int):
        query = (
            select(PermissionModel)
            .join(
                RolePermissionModel,
                RolePermissionModel.permission_id == PermissionModel.id,
            )
            .join(RoleModel, RoleModel.id == RolePermissionModel.role_id)
            .where(
                RoleModel.id == role_id,
                RoleModel.is_active == True,
                RolePermissionModel.is_active == True,
                PermissionModel.is_active == True,
            )
        )

        result = await self.session.execute(query)
        permissions = result.scalars().all()

        return [
            PermissionBase.model_validate(permission, from_attributes=True)
            for permission in permissions
        ]

    async def get_all_by_user_id(self, user_id: int):
        query = (
            select(PermissionModel)
            .join(
                UserPermissionModel,
                UserPermissionModel.permission_id == PermissionModel.id,
            )
            .where(
                UserPermissionModel.user_id == user_id,
                PermissionModel.is_active == True,
                UserPermissionModel.is_active == True,
                PermissionModel.is_active == True,
            )
        )

        result = await self.session.execute(query)
        permissions = result.scalars().all()

        return [
            PermissionBase.model_validate(permission, from_attributes=True)
            for permission in permissions
        ]
