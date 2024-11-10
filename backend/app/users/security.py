from typing import Optional, Final, Union, Any

from app.core.db import AccessToken, get_access_token_db
from fastapi_users.authentication import JWTStrategy
from fastapi_users.jwt import SecretType, generate_jwt
from fastapi_users.authentication.strategy.db import AccessTokenDatabase, DatabaseStrategy
from fastapi import Depends

from app.core.config import get_config
from app.models.tables import User
from jose import jwt, JWTError


config = get_config()

JWT_HASHING_ALGORITHM: Final[str] = 'HS256'


class TodosJWTStrategy(JWTStrategy):
    def __init__(
            self,
            secret: SecretType,
            lifetime_seconds: Optional[int],
            token_audience: Optional[list[str]] = None,
            algorithm: str = JWT_HASHING_ALGORITHM,
            public_key: Optional[SecretType] = None,
    ):
        if token_audience is None:
            token_audience = ['fastapi-users:auth', 'fastapi-users:verify']

        compat_audience = (
            token_audience[0] 
            if isinstance(token_audience, list) 
            else token_audience
        )

        super().__init__(secret=secret, lifetime_seconds=lifetime_seconds,
                         token_audience=compat_audience, algorithm=algorithm,
                         public_key=public_key)
        
    def decode_jwt_token(self, token: str) -> dict[str, Any]:
        """Decode and validate JWT token with support for both audience types."""
        try:
            if isinstance(self.decode_key, str):
                key = self.decode_key
            else:
                key = self.decode_key.get_secret_value()

            # First try decoding with original audience format
            try:
                return jwt.decode(
                    token,
                    key,
                    algorithms=[self.algorithm],
                    audience=self.token_audience,
                )
            except JWTError as e:
                print(f"First decode attempt failed: {e}")
                # If that fails and we have a list of audiences,
                # try each one individually
                if isinstance(self.token_audience, list):
                    for aud in self.token_audience:
                        try:
                            return jwt.decode(
                                token,
                                key,
                                algorithms=[self.algorithm],
                                audience=aud,
                            )
                        except JWTError:
                            continue
                
                # If all attempts fail, try without audience validation
                decoded = jwt.decode(
                    token,
                    key,
                    algorithms=[self.algorithm],
                    options={"verify_aud": False}
                )
                
                # Verify audience manually for more flexible validation
                token_aud = decoded.get("aud")
                if token_aud:
                    if isinstance(token_aud, list):
                        if isinstance(self.token_audience, list):
                            if any(a in token_aud for a in self.token_audience):
                                return decoded
                        elif self.token_audience in token_aud:
                            return decoded
                    elif isinstance(self.token_audience, list):
                        if token_aud in self.token_audience:
                            return decoded
                    elif token_aud == self.token_audience:
                        return decoded
                
                raise JWTError("Invalid audience")
                
        except Exception as e:
            print(f"JWT decode error: {e}")
            raise

    async def read_token(self, token: str, user_manager=None) -> Optional[dict[str, Any]]:
        """Override read_token to handle custom audience"""
        try:
            data = self.decode_jwt_token(token)
            if isinstance(data.get("aud"), list):  # Handle list audience
                return data
            return None
        except Exception as e:
            print(f"Token validation error: {e}")  # Add debug print
            return None
        
    async def write_token(self, user: User) -> str:
        data = self.generate_jwt_data(user)
        return generate_jwt(data, self.encode_key, self.lifetime_seconds, algorithm=self.algorithm)

    def generate_jwt_data(self, user: User) -> dict[str, Union[str, list[str], bool]]:
        return dict(user_id=str(user.id),
                    aud=self.token_audience,
                    email=user.email,
                    isSuperuser=user.is_superuser)


class TodosDBStrategy(DatabaseStrategy):
    def __init__(self, *args, **kwargs):
        self.token_audience = kwargs.pop('token_audience', ['fastapi-users:auth', 'fastapi-users:verify'])
        self.encode_key = kwargs.pop('encode_key')
        self.lifetime_seconds = kwargs.pop('lifetime_seconds')
        self.algorithm = kwargs.pop('algorithm', JWT_HASHING_ALGORITHM)
        self.public_key = kwargs.pop('public_key')

        super().__init__(*args, **kwargs)
        

    async def read_token(self, token: str, user_manager=None) -> Optional[dict[str, Any]]:
        return await super().read_token(token, user_manager)
    
    async def write_token(self, user: User) -> str:
        data = self.generate_jwt_data(user)
        return generate_jwt(data, self.encode_key, self.lifetime_seconds, algorithm=self.algorithm)

    def generate_jwt_data(self, user: User) -> dict[str, Union[str, list[str], bool]]:
        return dict(user_id=str(user.id),
                    aud=self.token_audience,
                    email=user.email,
                    isSuperuser=user.is_superuser)
    
    

def get_jwt_strategy() -> JWTStrategy:
    return TodosJWTStrategy(
        secret=config.JWT_SECRET_KEY,
        algorithm=config.JWT_ALGORITHM,
        lifetime_seconds=config.JWT_LIFETIME_SECONDS,
        token_audience=['fastapi-users:auth', 'fastapi-users:verify']

    )


def get_database_strategy(
    access_token_db: AccessTokenDatabase[AccessToken] = Depends(get_access_token_db),
) -> DatabaseStrategy:
    return DatabaseStrategy(access_token_db,                             
                            lifetime_seconds=3600)


