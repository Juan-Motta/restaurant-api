from src.domain.entities.permission import PermissionBase


class IPermissionRepository:
    async def get_all_by_role_id(self, role_id: int) -> list[PermissionBase]:
        raise NotImplementedError

    async def get_all_by_user_id(self, user_id: int) -> list[PermissionBase]:
        raise NotImplementedError
