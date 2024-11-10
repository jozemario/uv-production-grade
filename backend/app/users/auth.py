from asyncio.log import logger
from fastapi_users.authentication import AuthenticationBackend, BearerTransport
from fastapi import HTTPException
from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends
from app.users.security import get_database_strategy, get_jwt_strategy
from app.core.config import get_config
from fastapi.security import HTTPBearer
from typing import Optional
from fastapi import Request


config = get_config()


# bearer_transport = BearerTransport(tokenUrl=f'{config.API_V1_STR}/auth/login')
oauth2_scheme = OAuth2PasswordBearer(tokenUrl=f"{config.API_V1_STR}/auth/login", scheme_name="JWT",
    auto_error=True)

class CustomBearerTransport(BearerTransport):
    async def get_login_response(self, token: str) -> dict:

        user = await verify_token(token)
        user_id = user.get("user_id")
        return {
            "access_token": token,
            "token_type": "bearer",
            "user_id": user_id,
            "user": user

        }

    async def get_logout_response(self) -> dict:
        return {"detail": "Successfully logged out"}
    
bearer_transport = CustomBearerTransport(tokenUrl=f'{config.API_V1_STR}/auth/login')

class HTTPBearerTokenOnly(HTTPBearer):
    async def __call__(self, request: Request) -> Optional[str]:  # type: ignore
        credentials = await super().__call__(request)
        if credentials:
            return credentials.credentials
        return None


class SimpleBearerTransport(BearerTransport):
    def __init__(self):
        self.scheme = HTTPBearerTokenOnly()  # type: ignore

bearer_db_transport = SimpleBearerTransport()

auth_backend = AuthenticationBackend(
    name='jwt',
    transport=bearer_transport,
    get_strategy=get_jwt_strategy
)

auth_db_backend = AuthenticationBackend(
    name="database",
    transport=bearer_db_transport,
    # transport=bearer_transport,
    get_strategy=get_database_strategy,
)

async def verify_token(token: str):
    try:
        strategy = get_jwt_strategy()
        # Test raw decode
        decoded = strategy.decode_jwt_token(token)
        # Test full validation
        validated = await strategy.read_token(token)
        return {
            "token_type": "Bearer",
            "valid": True,
            "decoded": decoded,
            "validated": validated,
            "audiences": decoded.get("aud", []),
            "user_id": decoded.get("user_id"),
            "email": decoded.get("email")
        }
    except Exception as e:
        raise HTTPException(
            status_code=401,
            detail=f"Token validation failed: {str(e)}",
            headers={"WWW-Authenticate": "Bearer"},
        )
    


async def validate_token(token: str = Depends(oauth2_scheme)) -> dict:
    """Validate token and return decoded data"""
    try:
        strategy = get_jwt_strategy()
        decoded = strategy.decode_jwt_token(token)
        validated = await strategy.read_token(token)
        if not validated:
            raise HTTPException(
                status_code=401,
                detail="Token validation failed",
                headers={"WWW-Authenticate": "Bearer"},
            )
        return decoded
    except Exception as e:
        raise HTTPException(
            status_code=401,
            detail=f"Token validation failed: {str(e)}",
            headers={"WWW-Authenticate": "Bearer"},
        )