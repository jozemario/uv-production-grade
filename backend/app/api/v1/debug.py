from asyncio.log import logger
from app.users.security import get_jwt_strategy
from app.users.auth import verify_token
from app.core.db import get_async_session
from fastapi import APIRouter, Depends, Request, HTTPException
from app.core.config import get_config
from typing import Dict
from app.users.auth import oauth2_scheme
from sqlalchemy.ext.asyncio import AsyncSession

config = get_config()


router = APIRouter(
    prefix="/debug", 
    tags=["Debug"], 
    dependencies=[
        Depends(oauth2_scheme),
        Depends(get_async_session)
    ]
)

@router.get("/verify-token")
async def verify_token_api(
    token: str = Depends(oauth2_scheme),
    session: AsyncSession = Depends(get_async_session)
    ):
    try:
        current_user = await verify_token(token)
        logger.info(f"Session: {str(session)}")
  
        return current_user
    except Exception as e:
        raise HTTPException(
            status_code=401,
            detail=f"Token validation failed: {str(e)}",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
@router.get("/auth-flow")
async def test_auth_flow(
    request: Request,
    token: str = Depends(oauth2_scheme),
):  
    logger.info(f"auth-flow Token: {token}")
    # Get the authorization header
    auth_header = request.headers.get('authorization')
    
    current_user = await verify_token(token)

    # Get the strategy
    strategy = get_jwt_strategy()
    
    # Try to decode the token
    token = auth_header.split(' ')[1] if auth_header else None
    decoded = None
    if token:
        try:
            decoded = await strategy.read_token(token)
        except Exception as e:
            decoded = f"Error decoding token: {str(e)}"
    
    return {
        "auth_header_present": bool(auth_header),
        "token_format": "Bearer" if auth_header and auth_header.startswith('Bearer ') else "Invalid",
        "token_decoded": decoded is not None,
        "user_authenticated": bool(current_user),
        "user_id": str(current_user) if current_user else None,
    }
