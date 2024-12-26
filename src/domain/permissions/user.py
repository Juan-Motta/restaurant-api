from src.domain.constants.enums import (
    PermissionActionEnum,
    PermissionOwnerEnum,
    PermissionResourceEnum,
)
from src.domain.permissions.base import PermissionBase


class ReadAnyUsers(PermissionBase):
    action = PermissionActionEnum.READ.value
    owner = PermissionOwnerEnum.ANY.value
    resource = PermissionResourceEnum.USER.value


class CreateAnyUsers(PermissionBase):
    action = PermissionActionEnum.CREATE.value
    owner = PermissionOwnerEnum.ANY.value
    resource = PermissionResourceEnum.USER.value


class UpdateAnyUsers(PermissionBase):
    action = PermissionActionEnum.UPDATE.value
    owner = PermissionOwnerEnum.ANY.value
    resource = PermissionResourceEnum.USER.value


class DeactivateAnyUsers(PermissionBase):
    action = PermissionActionEnum.DEACTIVATE.value
    owner = PermissionOwnerEnum.ANY.value
    resource = PermissionResourceEnum.USER.value


class ReadOwnUsers(PermissionBase):
    action = PermissionActionEnum.READ.value
    owner = PermissionOwnerEnum.OWN.value
    resource = PermissionResourceEnum.USER.value


class UpdateOwnUsers(PermissionBase):
    action = PermissionActionEnum.UPDATE.value
    owner = PermissionOwnerEnum.OWN.value
    resource = PermissionResourceEnum.USER.value


class DeactivateOwnUsers(PermissionBase):
    action = PermissionActionEnum.DEACTIVATE.value
    owner = PermissionOwnerEnum.OWN.value
    resource = PermissionResourceEnum.USER.value


class DeleteOwnUsers(PermissionBase):
    action = PermissionActionEnum.DELETE.value
    owner = PermissionOwnerEnum.OWN.value
    resource = PermissionResourceEnum.USER.value
