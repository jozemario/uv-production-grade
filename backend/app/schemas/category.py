from uuid import UUID
from typing import Optional

from pydantic import BaseModel

from app.schemas.base import BaseInDB
from app.models.tables import Category


class CategoryCreate(BaseModel):
    name: str


class CategoryRead(CategoryCreate):
    id: UUID
    created_by_id: Optional[UUID]

    class Config:
        from_attributes = True


class CategoryInDB(BaseInDB, CategoryCreate):
    created_by_id: Optional[UUID]

    class Config(BaseInDB.Config):
        orm_model = Category
