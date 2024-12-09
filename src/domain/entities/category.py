from pydantic import BaseModel, ConfigDict


class Category(BaseModel):
    id: int
    name: str
    description: str
    typology: str
    is_active: bool

    model_config = ConfigDict(from_attributes=True)
