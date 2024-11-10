from typing import Union
from uuid import uuid4

from fastapi_users.db import SQLAlchemyBaseUserTableUUID
from fastapi_users_db_sqlalchemy import GUID
from sqlalchemy import Column, ForeignKey, Text, String, Boolean, UniqueConstraint, UUID
from sqlalchemy.orm import relationship, RelationshipProperty, Mapped

from app.models.base import Base


class User(SQLAlchemyBaseUserTableUUID, Base):
    """User model inheriting from FastAPI Users and our Base"""
    # Additional fields can be added here if needed
    pass


class Priority(Base):
    id = Column( UUID(), default=uuid4, primary_key=True)
    name = Column(String(15), nullable=False, unique=True)

    todos: Mapped[list["Todo"]] = relationship("Todo", back_populates="priority", lazy='selectin')


class Category(Base):
    id = Column(UUID(), default=uuid4, primary_key=True)
    name = Column(Text(), nullable=False)
    # Default categories are those where created_by_id is NULL,
    # indicating they are created by the system and are applicable to all users
    created_by_id = Column(GUID, ForeignKey('user.id'))

    __table_args__ = (
        UniqueConstraint('name', 'created_by_id', name='unique_category'),
    )

     # Update relationships
    todos_categories: Mapped[list["TodoCategory"]] = relationship(
        'TodoCategory',
        back_populates='category',
        cascade='all, delete-orphan',
        lazy='selectin'
    )
    
    todos: Mapped[list["Todo"]] = relationship(
        'Todo',
        secondary='todo_category',
        back_populates='categories',
        viewonly=True,
        lazy='selectin'
    )

    user: Mapped["User"] = relationship("User", backref="categories")


class Todo(Base):
    id = Column(UUID(), default=uuid4, primary_key=True)
    is_completed = Column(Boolean(), nullable=False, default=False)
    content = Column(Text(), nullable=False)
    created_by_id = Column(GUID, ForeignKey('user.id'), nullable=False)
    priority_id = Column(UUID, ForeignKey('priority.id'), nullable=False)

     # Update relationships
    priority: Mapped["Priority"] = relationship('Priority', back_populates='todos', lazy='selectin')
    categories: Mapped[list["Category"]] = relationship(
        'Category',
        secondary='todo_category',
        back_populates='todos',
        viewonly=True,
        lazy='selectin'
    )
    todos_categories: Mapped[list["TodoCategory"]] = relationship(
        'TodoCategory',
        back_populates='todo',
        cascade='all, delete-orphan',
        lazy='selectin'
    )
    user: Mapped["User"] = relationship("User", backref="todos")

    def dict(self) -> dict:
        todo_dict: dict[str, Union[str, str, bool]] = super().dict()
        todo_dict['todos_categories'] = self.todos_categories
        return todo_dict


class TodoCategory(Base):
    todo_id = Column(
        UUID,
        ForeignKey('todo.id', ondelete='CASCADE'),
        primary_key=True
    )
    category_id = Column(
        UUID,
        ForeignKey('category.id', ondelete='CASCADE'),
        primary_key=True
    )

    # Update relationships
    todo: Mapped["Todo"] = relationship(
        'Todo',
        back_populates='todos_categories',
        lazy='selectin'
    )
    category: Mapped["Category"] = relationship(
        'Category',
        back_populates='todos_categories',
        lazy='selectin'
    )
