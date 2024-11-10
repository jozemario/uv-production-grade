from app.models.tables import User
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.users.auth import oauth2_scheme, verify_token
from app.users.users import fast_api_users
from app.schemas import UserRead, UserUpdate
# from app.users.users import current_active_user
from app.core.db import get_async_session


router = APIRouter(
    prefix='/users',
    tags=['Users'],
    dependencies=[
        Depends(oauth2_scheme),
        Depends(get_async_session)
    ]
)

router.include_router(fast_api_users.get_users_router(UserRead, UserUpdate))

@router.get("/me")
async def get_current_user(
    session: AsyncSession = Depends(get_async_session),
    token: str = Depends(oauth2_scheme)
):
    user = await verify_token(token)
    return user
