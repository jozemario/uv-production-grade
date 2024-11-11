from asyncio.log import logger
from uuid import UUID
from typing import Optional

from sqlalchemy import or_, and_
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.dal.db_repo import DBRepo
from app.dal.constants import GET_MULTI_DEFAULT_SKIP, GET_MULTI_DEFAULT_LIMIT
from app.models.tables import Priority, Category, Todo, TodoCategory
from app.schemas import CategoryInDB, TodoInDB, TodoUpdateInDB
from app.http_exceptions import ResourceNotExists, UserNotAllowed, ResourceAlreadyExists
from app.websockets.manager import websocket_manager
from app.api.v1.webhooks import notify_webhooks

class DBService:

    def __init__(self) -> None:
        self._repo = DBRepo()

    async def _validate_todo_categories(
        self,
        session: AsyncSession,
        *,
        todo_categories_ids: list[UUID],
        created_by_id: UUID
    ) -> bool:
        # validates that the todo categories are valid to the user + no duplications
        default_categories_filter = Category.created_by_id.is_(None)
        user_categories_filter = Category.created_by_id == created_by_id
        valid_categories_filter = or_(default_categories_filter, user_categories_filter)
        todo_categories_ids_filter = Category.id.in_(todo_categories_ids)

        categories_from_db: list[Category] = await self._repo.get_multi(
            session,
            table_model=Category,
            query_filter=and_(valid_categories_filter, todo_categories_ids_filter)
        )
        are_categories_valid: bool = len(todo_categories_ids) == len(categories_from_db)
        return are_categories_valid

    async def get_priorities(self, session: AsyncSession) -> list[Priority]:
        return await self._repo.get_multi(session, table_model=Priority)

    async def get_categories(
        self,
        session: AsyncSession,
        *,
        created_by_id: UUID,
        skip: int = GET_MULTI_DEFAULT_SKIP,
        limit: int = GET_MULTI_DEFAULT_LIMIT
    ) -> list[Category]:
        default_categories_filter = Category.created_by_id.is_(None)
        user_categories_filter = Category.created_by_id == created_by_id
        query_filter = or_(user_categories_filter, default_categories_filter)
        return await self._repo.get_multi(
            session,
            table_model=Category,
            query_filter=query_filter,
            limit=limit,
            skip=skip
        )

    async def add_category(
        self,
        session: AsyncSession,
        *,
        category_in: CategoryInDB
    ) -> Category:
        users_categories: list[Category] = await self.get_categories(
            session,
            created_by_id=category_in.created_by_id)
        users_categories_names: list[str] = [c.name for c in users_categories]
        if category_in.name in users_categories_names:
            raise ResourceAlreadyExists(resource='category name')
        return await self._repo.create(session, obj_to_create=category_in)

    async def delete_category(
        self,
        session: AsyncSession,
        *,
        id_to_delete: UUID,
        created_by_id: UUID
    ) -> None:
        category_to_delete: Optional[Category] = await self._repo.get(
            session,
            table_model=Category,
            query_filter=Category.id == id_to_delete
        )
        if not category_to_delete:
            raise ResourceNotExists(resource='category')
        if category_to_delete.created_by_id != created_by_id:
            raise UserNotAllowed('a user can not delete a category that was not created by him')
        await self._repo.delete(session, table_model=Category, id_to_delete=id_to_delete)

    async def get_todos(
        self,
        session: AsyncSession,
        *,
        created_by_id: UUID,
        skip: int = GET_MULTI_DEFAULT_SKIP,
        limit: int = GET_MULTI_DEFAULT_LIMIT
    ) -> list[Todo]:
        return await self._repo.get_multi(
            session,
            table_model=Todo,
            query_filter=Todo.created_by_id == created_by_id,
            skip=skip,
            limit=limit
        )

    async def add_todo(
        self,
        session: AsyncSession,
        *,
        todo_in: TodoInDB
    ) -> Todo:
        if await self._validate_todo_categories(
            session,
            todo_categories_ids=todo_in.categories_ids,
            created_by_id=todo_in.created_by_id
        ):
            try:
                return await self._repo.create(session, obj_to_create=todo_in)
            except IntegrityError:
                raise ValueError('priority is not valid')
        raise ValueError('categories are not valid')
    async def update_todo(
        self,
        session: AsyncSession,
        *,
        updated_todo: TodoUpdateInDB
    ) -> Todo:
        todo_to_update: Optional[Todo] = await self._repo.get(
            session,
            table_model=Todo,
            query_filter=Todo.id == updated_todo.id
        )
        if not todo_to_update:
            raise ResourceNotExists(resource='todo')
        if not todo_to_update.created_by_id == updated_todo.created_by_id:
            raise UserNotAllowed('a user can not update a todo that was not created by him')
        
        if await self._validate_todo_categories(
            session,
            todo_categories_ids=updated_todo.categories_ids,
            created_by_id=updated_todo.created_by_id
        ):
            try:
                # Update the existing todo's attributes
                todo_to_update.content = updated_todo.content
                todo_to_update.is_completed = updated_todo.is_completed
                todo_to_update.priority_id = updated_todo.priority_id
                
                # Clear and recreate category relationships
                todo_to_update.todos_categories = []
                await session.flush()
                
                todo_to_update.todos_categories = [
                    TodoCategory(category_id=c_id) 
                    for c_id in updated_todo.categories_ids
                ]
                
                # Commit the changes
                await session.commit()
                return todo_to_update
                
            except IntegrityError as e:
                logger.error(f"IntegrityError during todo update: {e}")
                await session.rollback()
                raise ValueError('priority is not valid')
        raise ValueError('categories are not valid')
   
    async def delete_todo(
    self,
    session: AsyncSession,
    *,
    id_to_delete: UUID,
    created_by_id: UUID
) -> None:
        try:
            # Get the todo with all its relationships
            todo_to_delete: Optional[Todo] = await self._repo.get(
                session,
                table_model=Todo,
                query_filter=Todo.id == id_to_delete
            )

            if not todo_to_delete:
                logger.error(f"Todo with id {id_to_delete} not found")
                raise ResourceNotExists(resource='todo')

            # Convert UUIDs to strings for comparison
            todo_user_id = str(todo_to_delete.created_by_id)
            request_user_id = str(created_by_id)
            
            logger.info(f"Todo user ID: {todo_user_id}, Request user ID: {request_user_id}")
                
            if todo_user_id != request_user_id:
                logger.error(f"User {created_by_id} attempted to delete todo owned by {todo_to_delete.created_by_id}")
                raise UserNotAllowed('a user can not delete a todo that was not created by him')
            
            # Delete related todo_category entries first
            if todo_to_delete.todos_categories:
                todo_to_delete.todos_categories = []
                await session.flush()
            
            # Delete the todo
            await self._repo.delete(session, table_model=Todo, id_to_delete=id_to_delete)
            await session.commit()
            
            logger.info(f"Successfully deleted todo {id_to_delete}")
            
        except IntegrityError as e:
            logger.error(f"Error deleting todo {id_to_delete}: {e}")
            await session.rollback()
            raise
        except Exception as e:
            logger.error(f"Unexpected error deleting todo {id_to_delete}: {e}")
            await session.rollback()
            raise

    async def notify_todo_update(
        self,
        session: AsyncSession,
        user_id: UUID,
        event_type: str,
        todo_data: dict
    ):
        # Notify via WebSocket
        await websocket_manager.broadcast_to_user(
            str(user_id),
            {
                "type": event_type,
                "data": todo_data
            }
        )
        
        # Notify via webhooks
        await notify_webhooks(session, user_id, event_type, todo_data)


db_service = DBService()
