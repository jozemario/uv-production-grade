from asyncio.log import logger
from uuid import UUID
from fastapi import APIRouter, status, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from pydantic import conint

from app.core.db import get_async_session
# from app.users.users import current_logged_user
from app.dal import db_service, GET_MULTI_DEFAULT_SKIP, GET_MULTI_DEFAULT_LIMIT, MAX_POSTGRES_INTEGER
from app.schemas import CategoryCreate, CategoryRead, CategoryInDB
from app.models.tables import Category
from app.utils import exception_handler, get_open_api_response, get_open_api_unauthorized_access_response
from app.users.auth import oauth2_scheme, verify_token

router = APIRouter(
    prefix='/categories',
    dependencies=[
        Depends(oauth2_scheme),
        Depends(get_async_session)
    ],
    tags=['Categories']
)


@router.get(
    '',
    response_model=list[CategoryRead],
    responses={status.HTTP_401_UNAUTHORIZED: get_open_api_unauthorized_access_response()}
)
async def get_categories(
    skip: conint(ge=0, le=MAX_POSTGRES_INTEGER) = GET_MULTI_DEFAULT_SKIP,  # type: ignore[valid-type]
    limit: conint(ge=0, le=MAX_POSTGRES_INTEGER) = GET_MULTI_DEFAULT_LIMIT,  # type: ignore[valid-type]
    session: AsyncSession = Depends(get_async_session),
    token: str = Depends(oauth2_scheme)
) -> list[Category]:
    user = await verify_token(token)
    try:
        return await db_service.get_categories(
            session,
            created_by_id=user.get("user_id"),
            skip=skip,
            limit=limit
        )
    except Exception as e:
        raise HTTPException(status_code=401, detail=str(e))


@router.post(
    '',
    response_model=CategoryRead,
    status_code=status.HTTP_201_CREATED,
    responses={
        status.HTTP_401_UNAUTHORIZED: get_open_api_unauthorized_access_response(),
        status.HTTP_400_BAD_REQUEST: get_open_api_response(
            {'Trying to add an existing category': 'category name already exists'}
        )
    }
)
@exception_handler
async def add_category(
    category_in: CategoryCreate,
    session: AsyncSession = Depends(get_async_session),
    token: str = Depends(oauth2_scheme) 
) -> Category:
        user = await verify_token(token)
        category_in = CategoryInDB(name=category_in.name, created_by_id=user.get("user_id"))
        return await db_service.add_category(session, category_in=category_in)


@router.delete(
    '/{category_id}',
    status_code=status.HTTP_204_NO_CONTENT,
    responses={
        status.HTTP_401_UNAUTHORIZED: get_open_api_unauthorized_access_response(),
        status.HTTP_403_FORBIDDEN: get_open_api_response(
            {'Trying to delete system or another users category':
             'a user can not delete a category that was not created by him'}
        ),
        status.HTTP_404_NOT_FOUND: get_open_api_response(
            {'Trying to delete non existing category': 'category does not exists'}
        )
    }
)
@exception_handler
async def delete_category(
    category_id: UUID,
    token: str = Depends(oauth2_scheme),
    session: AsyncSession = Depends(get_async_session)
) -> None:
    user = await verify_token(token)
    user_id = UUID(user.get("user_id"))  # Convert string to UUID
    logger.info(f"Deleting category: {category_id} by user: {user_id}")
    await db_service.delete_category(session, id_to_delete=category_id, created_by_id=user_id)

