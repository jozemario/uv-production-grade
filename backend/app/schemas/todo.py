from uuid import UUID

from pydantic import BaseModel

from app.schemas.base import BaseInDB, BaseUpdateInDB
from app.schemas.priority import PriorityRead
from app.schemas.category import CategoryRead
from app.models.tables import Todo, TodoCategory


class TodoBase(BaseModel):
    content: str


class TodoRead(TodoBase):
    id: UUID
    is_completed: bool
    priority: PriorityRead
    categories: list[CategoryRead]

    class Config:
        from_attributes = True


class TodoCreate(TodoBase):
    priority_id: UUID
    categories_ids: list[UUID]


class TodoInDB(BaseInDB, TodoCreate):
    created_by_id: UUID
    priority_id: UUID

    class Config(BaseInDB.Config):
        orm_model = Todo

    def to_orm(self) -> Todo:
        # converts categories_ids to todos_categories
        orm_data = dict(self)
        categories_ids = orm_data.pop('categories_ids')
        todo_orm = self.Config.orm_model(**orm_data)
        todo_orm.todos_categories = [TodoCategory(category_id=c_id) for c_id in categories_ids]
        return todo_orm


class TodoUpdate(TodoCreate):
    is_completed: bool


class TodoUpdateInDB(BaseUpdateInDB, TodoInDB):
    is_completed: bool
