from pydantic import BaseModel


class PermissionBase(BaseModel):
    id: int
    name: str
    slug: str
    description: str
    is_active: bool
