from asyncio.log import logger
from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from pydantic import conint
from uuid import UUID
from app.core.db import User, get_async_session
from app.models.tables import Todo
from app.dal import db_service, GET_MULTI_DEFAULT_SKIP, GET_MULTI_DEFAULT_LIMIT, MAX_POSTGRES_INTEGER
from app.schemas import TodoRead, TodoInDB, TodoCreate, TodoUpdate, TodoUpdateInDB
from app.utils import exception_handler, get_open_api_response, get_open_api_unauthorized_access_response
from app.core.config import get_config
from app.users.auth import oauth2_scheme, verify_token, validate_token
from app.users.users import current_active_user
config = get_config()



router = APIRouter(
    prefix='/todos',
    dependencies=[
        Depends(oauth2_scheme),
        Depends(get_async_session)
    ],
    tags=['Todos']
)
   
@router.get(
    '',
    response_model=list[TodoRead],
    responses={status.HTTP_401_UNAUTHORIZED: get_open_api_unauthorized_access_response()}
)
@exception_handler
async def get_todos(
    skip: conint(ge=0, le=MAX_POSTGRES_INTEGER) = GET_MULTI_DEFAULT_SKIP,  # type: ignore[valid-type]
    limit: conint(ge=0, le=MAX_POSTGRES_INTEGER) = GET_MULTI_DEFAULT_LIMIT,  # type: ignore[valid-type]
    token: str = Depends(oauth2_scheme),
    session: AsyncSession = Depends(get_async_session),
) -> Todo:
    user = await verify_token(token)
    logger.info(f"Getting todos for user {user}")
    logger.info(f"current_active_user: {current_active_user}")

    # logger.info(f"current_logged_user: {current_logged_user}")

    return await db_service.get_todos(
            session,
            created_by_id=user.get("user_id"),
            skip=skip,
            limit=limit
            )
        

@router.post(
    '',
    response_model=TodoRead,
    status_code=status.HTTP_201_CREATED,
    responses={
        status.HTTP_401_UNAUTHORIZED: get_open_api_unauthorized_access_response(),
        status.HTTP_400_BAD_REQUEST: get_open_api_response(
            {
                'Trying to connect duplicate categories or another users category': 'categories are not valid',
                'Trying to connect non existing priority': 'priority is not valid'
            }
        )

    }
)
@exception_handler
async def add_todo(
    todo_in: TodoCreate,
    token: str = Depends(oauth2_scheme),
    session: AsyncSession = Depends(get_async_session)
) -> Todo:
    user = await verify_token(token)
    user_id = UUID(user.get("user_id"))
    
    todo_in = TodoInDB(
        content=todo_in.content,
        priority_id=todo_in.priority_id,
        categories_ids=todo_in.categories_ids,
        created_by_id=user_id
    )
    
    new_todo = await db_service.add_todo(session, todo_in=todo_in)
    
    # Notify about the new todo
    await db_service.notify_todo_update(
        session,
        user_id,
        "todo.created",
        new_todo.dict()
    )
    
    return new_todo


@router.put(
    '/{todo_id}',
    response_model=TodoRead,
    responses={
        status.HTTP_401_UNAUTHORIZED: get_open_api_unauthorized_access_response(),
        status.HTTP_400_BAD_REQUEST: get_open_api_response(
            {
                'Trying to connect duplicate categories or another users category': 'categories are not valid',
                'Trying to connect non existing priority': 'priority is not valid'
            }
        ),
        status.HTTP_403_FORBIDDEN: get_open_api_response(
            {'Trying to update another users todo':
             'a user can not update a todo that was not created by him'}
        ),
        status.HTTP_404_NOT_FOUND: get_open_api_response(
            {'Trying to update non existing todo': 'todo does not exists'}
        )
    }
)
@exception_handler
async def update_todo(
    todo_id: str,
    updated_todo: TodoUpdate,
    token: str = Depends(oauth2_scheme),
    session: AsyncSession = Depends(get_async_session)
) -> Todo:
    user = await verify_token(token)

    logger.info(f"Updated todo: {updated_todo}")
    updated_todo = TodoUpdateInDB(
        id=todo_id,
        content=updated_todo.content,
        priority_id=updated_todo.priority_id,
        categories_ids=updated_todo.categories_ids,
        is_completed=updated_todo.is_completed,
        created_by_id=user.get("user_id")
    )
    updated_todo = await db_service.update_todo(session, updated_todo=updated_todo)
    
    # Notify about the updated todo
    await db_service.notify_todo_update(
        session,
        user.get("user_id"),
        "todo.updated",
        updated_todo.dict()
    )
  
    return updated_todo


@router.delete(
    '/{todo_id}',
    status_code=status.HTTP_204_NO_CONTENT,
    responses={
        status.HTTP_401_UNAUTHORIZED: get_open_api_unauthorized_access_response(),
        status.HTTP_403_FORBIDDEN: get_open_api_response(
            {'Trying to update another users todo':
             'a user can not update a todo that was not created by him'}
        ),
        status.HTTP_404_NOT_FOUND: get_open_api_response(
            {'Trying to update non existing todo': 'todo does not exists'}
        )
    }
)
@exception_handler
async def delete_todo(
    todo_id: UUID,
    token: str = Depends(oauth2_scheme),
    session: AsyncSession = Depends(get_async_session)
) -> None:
    user = await verify_token(token)
    user_id = UUID(user.get("user_id"))  # Convert string to UUID
    logger.info(f"Attempting to delete todo {todo_id} by user {user_id}")

    await db_service.delete_todo(session, id_to_delete=todo_id, created_by_id=user_id)
    
    # Notify about the deleted todo
    await db_service.notify_todo_update(
        session,
        user_id,
        "todo.deleted",
        {"id": todo_id}
    )