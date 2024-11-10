from typing import Final, Optional, AsyncGenerator
import json
import logging
from pathlib import Path

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import create_db_and_tables, get_async_session, engine
from app.models.tables import Priority, Category, User
from app.schemas.category import CategoryInDB
from app.core.config import get_config

logger = logging.getLogger(__name__)

INITIAL_DATA_FILE_PATH: Final[str] = Path(__file__).parent.parent / 'scripts' / 'initial_data.json'

async def get_priority_by_name(session: AsyncSession, name: str) -> Optional[Priority]:
    result = await session.execute(
        select(Priority).filter(Priority.name == name)
    )
    return result.scalar_one_or_none()

async def get_category_by_name(session: AsyncSession, name: str) -> Optional[Category]:
    result = await session.execute(
        select(Category).filter(Category.name == name)
    )
    return result.scalar_one_or_none()


async def init_priorities(session: AsyncSession, priorities_names: list[str]) -> None:
    """Initialize default priorities if they don't exist."""
    for priority_name in priorities_names:
        existing_priority = await get_priority_by_name(session, priority_name)
        if not existing_priority:
            priority = Priority(name=priority_name)
            session.add(priority)
            logger.info(f"Created priority: {priority_name}")

async def init_categories(session: AsyncSession, categories_names: list[str]) -> None:
    """Initialize default categories if they don't exist."""
    for category_name in categories_names:
        existing_category = await get_category_by_name(session, category_name)
        if not existing_category:
            category_in = CategoryInDB(
                name=category_name,
                created_by_id=None  # System-created categories have no user
            )
            category = category_in.to_orm()
            session.add(category)
            logger.info(f"Created category: {category_name}")
      
            

async def init_db() -> None:
    """Initialize database with default data."""
    try:
        # Read initial data
        with open(INITIAL_DATA_FILE_PATH, 'r') as f:
            initial_data: dict[str, list[str]] = json.load(f)

        logger.info("Creating initial data")
        
        async for session in get_async_session():
            #Init auth tables
            await create_db_and_tables()
            # Initialize priorities
            await init_priorities(session, initial_data["priorities_names"])
            
            # Initialize categories
            await init_categories(session, initial_data["categories_names"])
            
            await session.commit()
            
        logger.info("Initial data created successfully")
        
    except Exception as e:
        logger.error(f"Error creating initial data: {e}")
        raise

async def init_app() -> None:
    """Initialize the application."""
    config = get_config()
    
    logger.info("Initializing application")
    
    # Initialize database with default data
    await init_db()
    
    logger.info("Application initialized successfully")

# Script execution part
if __name__ == "__main__":
    import asyncio
    from app.core.db import engine
    
    async def init_script() -> None:
        try:
            await init_db()
        finally:
            await engine.dispose()

    asyncio.run(init_script())