from asyncio.log import logger
from fastapi import APIRouter
from fastapi import Depends
from app.users.users import fast_api_users
from app.users.auth import auth_backend
from app.schemas import UserRead, UserCreate
from app.users.auth import oauth2_scheme, verify_token, bearer_transport, bearer_db_transport


router = APIRouter(
    prefix='/auth',
    tags=['Auth']
)

router.include_router(fast_api_users.get_auth_router(auth_backend))
# router.include_router(fast_api_users.get_auth_router(auth_db_backend))
router.include_router(fast_api_users.get_register_router(UserRead, UserCreate))
router.include_router(fast_api_users.get_reset_password_router())
router.include_router(fast_api_users.get_verify_router(UserRead))

@router.post("/custom-logout")
async def custom_logout(
    token: str = Depends(oauth2_scheme),
):  
    user = await verify_token(token)
    logger.info("Custom logout endpoint")
    logger.info(user)
    logger.info(token)
    await bearer_transport.get_logout_response()
    # return {"message": "Logged out"}

