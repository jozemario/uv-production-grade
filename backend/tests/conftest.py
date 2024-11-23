import json
import os
import pytest
import asyncio
from typing import AsyncGenerator, Generator
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from fastapi import FastAPI
from main import app  # Direct import of the app instance
from app.core.db import Base
from app.users.auth import create_access_token
from app.models.tables import User, Priority, Category, Todo

# Set test environment variables before importing app code
os.environ.update({
    "JWT_SECRET_KEY": "test_secret_key",
    "ENVIRONMENT": "test",
    "DATABASE_URL": "postgresql+asyncpg://user:password@localhost:5432/test_db",
    "JWT_SECRET": "test_secret",
    "POSTGRES_DB": "test_db",
    "POSTGRES_HOST": "localhost",
    "POSTGRES_USER": "postgres",
    "POSTGRES_PASSWORD": "postgres",
    "FRONT_END_BASE_URL": "http://localhost:3000",
    "NODE_ENV": "test"
})

# Test database URL
TEST_DATABASE_URL = os.environ["DATABASE_URL"]

# Create async engine for tests
engine = create_async_engine(TEST_DATABASE_URL, echo=True)
async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

# config = get_config()

def get_tests_data():
    with open('tests/tests_data.json', 'r') as file:
        return json.load(file)

@pytest.fixture(scope="session")
def event_loop() -> Generator:
    try:
        loop = asyncio.get_event_loop()
    except RuntimeError:
        loop = asyncio.new_event_loop()
    yield loop
    loop.close()

@pytest.fixture(scope="session")
async def test_app() -> FastAPI:
    return app

@pytest.fixture
async def client(test_app: FastAPI) -> AsyncClient:
    async with AsyncClient(
        app=test_app,
        base_url="http://test",
        headers={"Content-Type": "application/json"}
    ) as ac:
        yield ac

@pytest.fixture(scope="session")
async def db_engine():
    engine = create_async_engine(TEST_DATABASE_URL, echo=True)
    yield engine
    await engine.dispose()

@pytest.fixture(scope="function")
async def db_session():
    engine = create_async_engine(TEST_DATABASE_URL, echo=True)
    
    # Create all tables from scratch
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
    
    # Create session
    async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
    
    async with async_session() as session:
        # Get test data
        test_data = get_tests_data()
        user_data = test_data['users'][0]
        
        # Create test user
        user = User(
            id=user_data['id'],
            email=user_data['email']
        )
        session.add(user)
        
        # Create priorities
        priorities = [
            Priority(id="123e4567-e89b-12d3-a456-426614174001", name="High"),
            Priority(id="123e4567-e89b-12d3-a456-426614174002", name="Medium"),
            Priority(id="123e4567-e89b-12d3-a456-426614174003", name="Low")
        ]
        for priority in priorities:
            session.add(priority)
        
        # Create categories
        for category in user_data['categories']:
            cat = Category(
                id=category['id'],
                name=category['name'],
                created_by_id=user_data['id']
            )
            session.add(cat)
        
        await session.commit()
        
        yield session
    
    # Cleanup
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
    await engine.dispose()

@pytest.fixture(scope="session")
async def user_token_headers() -> dict:
    # Create a User instance instead of a dict
    test_user = User(
        id="123e4567-e89b-12d3-a456-426614174005",
        email="test@test.com",
        is_superuser=False
    )
    
    access_token = await create_access_token(
        test_user
    )
    return {"Authorization": f"Bearer {access_token}"}