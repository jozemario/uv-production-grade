import asyncio
from typing import Final, AsyncGenerator
import pytest
import pytest_asyncio
from httpx import AsyncClient
from asgi_lifespan import LifespanManager
from sqlalchemy.ext.asyncio import AsyncConnection, AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import create_async_engine
from app.core.config import get_test_config
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, async_sessionmaker, create_async_engine

# from app.core.db import Base

from main import app
from tests.conftest_utils import insert_test_data, get_user_token_headers

TEST_BASE_URL: Final[str] = 'http://test'

test_config = get_test_config()

engine:AsyncEngine = create_async_engine(str(test_config.POSTGRES_URI), echo=True)
async_session_maker = async_sessionmaker(engine, expire_on_commit=False)

async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_maker() as session:
        yield session

# Create async engine for testing
test_engine = create_async_engine(
    test_config.DATABASE_URL,
    echo=True,
    future=True
)

# Create async session factory
test_async_session = sessionmaker(
    test_engine, 
    class_=AsyncSession, 
    expire_on_commit=False
)

@pytest.fixture(scope='session')
def event_loop():
    policy = asyncio.get_event_loop_policy()
    loop = policy.new_event_loop()
    yield loop
    loop.close()

@pytest_asyncio.fixture(scope='session')
async def connection() -> AsyncGenerator[AsyncConnection, None]:
    async with engine.begin() as conn:
        yield conn
        await conn.rollback()

@pytest_asyncio.fixture(scope='session')
async def async_session(connection: AsyncConnection) -> AsyncGenerator[AsyncSession, None]:
    async with AsyncSession(connection, expire_on_commit=False) as session:
        yield session

@pytest_asyncio.fixture(scope='session', autouse=True)
async def create_test_data(async_session: AsyncSession):
    await insert_test_data(async_session)

@pytest_asyncio.fixture(autouse=True)
async def override_dependency(async_session: AsyncSession):
    app.dependency_overrides[get_async_session] = lambda: async_session
    yield
    app.dependency_overrides.clear()

@pytest_asyncio.fixture
async def client() -> AsyncGenerator[AsyncClient, None]:
    async with AsyncClient(app=app, base_url=TEST_BASE_URL) as ac, LifespanManager(app):
        yield ac

@pytest_asyncio.fixture
async def user_token_headers(client: AsyncClient) -> dict[str, str]:
    return await get_user_token_headers(client)

@pytest_asyncio.fixture(scope="session")
# async def test_db() -> AsyncGenerator:
#     async with test_engine.begin() as conn:
#         await conn.run_sync(Base.metadata.drop_all)
#         await conn.run_sync(Base.metadata.create_all)
#     yield
#     async with test_engine.begin() as conn:
#         await conn.run_sync(Base.metadata.drop_all)

@pytest_asyncio.fixture(scope="function")
async def test_session(test_db) -> AsyncGenerator[AsyncSession, None]:
    async with test_async_session() as session:
        yield session
        await session.rollback()
        await session.close()

@pytest.fixture(scope="function")
def override_get_config():
    return get_test_config()
