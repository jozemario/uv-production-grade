from asyncio.log import logger
from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_async_session
# from app.users.users import current_active_user
from app.dal import db_service
from app.models.tables import Priority
from app.schemas import PriorityRead
from app.utils import get_open_api_unauthorized_access_response
from app.users.auth import oauth2_scheme, verify_token

router = APIRouter(
    prefix='/priorities',
    dependencies=[
        Depends(oauth2_scheme),
        Depends(get_async_session)
    ],
    tags=['Priorities']
)


@router.get(
    '',
    response_model=list[PriorityRead],
    responses={status.HTTP_401_UNAUTHORIZED: get_open_api_unauthorized_access_response()}
)
async def get_priorities(
    token: str = Depends(oauth2_scheme),
    session: AsyncSession = Depends(get_async_session)
) -> Priority:
    try:
        user = await verify_token(token)
        logger.info(f"get_priorities: {user}")
        if user:
            return await db_service.get_priorities(session)
        else:
            raise HTTPException(status_code=401, detail="Unauthorized")
    except Exception as e:
        raise HTTPException(status_code=401, detail=str(e))
