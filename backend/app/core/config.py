from functools import lru_cache
import os
from typing import Any, Optional, List
import logging
from pydantic import  PostgresDsn, AnyHttpUrl, validator, SecretStr, EmailStr

from pydantic_settings import BaseSettings

logger = logging.getLogger(__name__)

class Settings(BaseSettings):
    DEBUG_MODE: bool = True  
    PROJECT_NAME: str = 'Todos API'
    PROJECT_VERSION: str = '1.0.0'
    API_V1_STR: str = '/api/v1'
    JWT_SECRET_KEY: SecretStr
    ENVIRONMENT: str 
    DATABASE_URL: str 
    @validator("DATABASE_URL", pre=True)
    def assemble_database_url(cls, v: Optional[str], values: dict[str, Any]) -> str:
        if isinstance(v, str):
            return v
        
        return str(PostgresDsn.build(
            scheme="postgresql+asyncpg",
            username=values.get("POSTGRES_USER"),
            password=values.get("POSTGRES_PASSWORD").get_secret_value(),
            host=values.get("POSTGRES_HOST", "localhost"),
            path=f"/{values.get('POSTGRES_DB', '')}",
        ))
    
    JWT_SECRET: str
    JWT_ALGORITHM: str = 'HS256'
    # 60 seconds by 60 minutes (1 hour) and then by 12 (for 12 hours total)
    JWT_LIFETIME_SECONDS: int = 60 * 60 * 12
    # Token audiences
    #JWT_TOKEN_AUDIENCES: List[str] = ["fastapi-users:auth", "fastapi-users:verify"]
    # CORS_ORIGINS is a string of ';' separated origins.
    # e.g:  'http://localhost:8080;http://localhost:3000'
    CORS_ORIGINS: Optional[str] = '*'
    POSTGRES_DB: str
    POSTGRES_HOST: str
    POSTGRES_USER: str
    POSTGRES_PASSWORD: SecretStr
    POSTGRES_URI: Optional[PostgresDsn] = None

    @validator('POSTGRES_URI', pre=True)
    def assemble_db_connection(cls, _: str, values: dict[str, Any]) -> str:
        postgres_password: SecretStr = values.get('POSTGRES_PASSWORD', SecretStr(''))
        return PostgresDsn.build(
            scheme='postgresql+asyncpg',
            #scheme='postgresql',
            username=values.get('POSTGRES_USER'),
            password=postgres_password.get_secret_value(),
            host=values.get('POSTGRES_HOST'),
            path=f'{values.get("POSTGRES_DB")}',
        )

    SMTP_TLS: bool = True
    SMTP_HOST: Optional[str] = None
    SMTP_PORT: Optional[int] = None
    SMTP_USER: Optional[str] = None
    SMTP_PASSWORD: Optional[SecretStr] = None
    EMAILS_FROM_EMAIL: Optional[EmailStr] = None
    EMAILS_FROM_NAME: Optional[str] = None

    @validator('EMAILS_FROM_NAME')
    def get_project_name(cls, v: Optional[str], values: dict[str, Any]) -> str:
        if not v:
            return values['PROJECT_NAME']
        return v

    EMAIL_TEMPLATES_DIR: str = './app/email-templates'
    EMAILS_ENABLED: bool = False

    @validator('EMAILS_ENABLED', pre=True)
    def get_emails_enabled(cls, _: bool, values: dict[str, Any]) -> bool:
        return all([
            values.get('SMTP_HOST'),
            values.get('SMTP_PORT'),
            values.get('EMAILS_FROM_EMAIL')
        ])

    # 60 seconds by 60 minutes (1 hour) and then by 12 (for 12 hours total)
    RESET_PASSWORD_TOKEN_LIFETIME_SECONDS: int = 60 * 60 * 12
    VERIFY_TOKEN_LIFETIME_SECONDS: int = 60 * 60 * 12

    FRONT_END_BASE_URL: AnyHttpUrl
    NODE_ENV: str

    class Config:
        # get environment from --env
        logger.info(f"Config ENVIRONMENT: {os.getenv('ENVIRONMENT')}")
        # env_file = '../.env.local'
        case_sensitive = True

        @classmethod
        def parse_env_var(cls, field_name: str, raw_val: str) -> Any:
            # if field_name == 'CORS_ORIGINS':
            #     return raw_val.split(',')
            # # The following line is ignored by mypy because:
            # error: Type'[Config]' has no attribute 'json_loads',
            # even though it is like the documentation: https://docs.pydantic.dev/latest/usage/settings/
            return cls.json_loads(raw_val)  # type: ignore[attr-defined]


class BaseAppSettings(BaseSettings):
    DEBUG_MODE: bool = True
    PROJECT_NAME: str = 'Todos API'
    PROJECT_VERSION: str = '1.0.0'
    API_V1_STR: str = '/api/v1'
    
    class Config:
        case_sensitive = True
class TestSettings(BaseAppSettings):
    ENVIRONMENT: str = "test"
    DATABASE_URL: str = "postgresql+asyncpg://user:password@localhost:5432/test_db"
    JWT_SECRET_KEY: SecretStr = SecretStr("test_secret_key")
    JWT_SECRET: str = "test_secret"
    JWT_ALGORITHM: str = 'HS256'
    JWT_LIFETIME_SECONDS: int = 60 * 60
    POSTGRES_DB: str = "test_db"
    POSTGRES_HOST: str = "localhost:5432"
    POSTGRES_USER: str = "user"
    POSTGRES_PASSWORD: SecretStr = SecretStr("password")
    FRONT_END_BASE_URL: AnyHttpUrl = "http://localhost:3000"
    NODE_ENV: str = "test"
    
    class Config:
        case_sensitive = True

@lru_cache()
def get_config() -> Settings:
    # TODO: remove 'type: ignore[call-arg]' once https://github.com/pydantic/pydantic/issues/3072 is closed
    return Settings()  # type: ignore[call-arg]

@lru_cache()
def get_test_config() -> TestSettings:
    return TestSettings()