from pydantic_settings import BaseSettings

class TestSettings(BaseSettings):
    JWT_SECRET_KEY: str = "test_secret_key"
    ENVIRONMENT: str = "test"
    DATABASE_URL: str = "postgresql+asyncpg://user:password@localhost:5432/test_db"
    JWT_SECRET: str = "test_secret"
    POSTGRES_DB: str = "test_db"
    POSTGRES_HOST: str = "localhost"
    POSTGRES_USER: str = "user"
    POSTGRES_PASSWORD: str = "password"
    POSTGRES_URI: str = "postgresql+asyncpg://user:password@localhost:5432/test_db"
    FRONT_END_BASE_URL: str = "http://localhost:3000"
    NODE_ENV: str = "test" 