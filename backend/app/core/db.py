from collections.abc import AsyncGenerator
from typing import Any
from fastapi_users.db import (
    SQLAlchemyBaseOAuthAccountTableUUID,
    SQLAlchemyBaseUserTableUUID,
    SQLAlchemyUserDatabase,
)
from fastapi_users_db_sqlalchemy.access_token import (
    SQLAlchemyAccessTokenDatabase,
    SQLAlchemyBaseAccessTokenTableUUID,
)
from fastapi import Depends

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import DeclarativeBase, Mapped, relationship

from app.core.config import get_config

config = get_config()

class Base(DeclarativeBase):
    pass


class OAuthAccount(SQLAlchemyBaseOAuthAccountTableUUID, Base):
    pass


class User(SQLAlchemyBaseUserTableUUID, Base):
    oauth_accounts: Mapped[list[OAuthAccount]] = relationship(
        "OAuthAccount", lazy="joined"
    )

class AccessToken(SQLAlchemyBaseAccessTokenTableUUID, Base):  
    pass

engine = create_async_engine(str(config.POSTGRES_URI), echo=True)
async_session_maker = async_sessionmaker(engine, expire_on_commit=False)



# engine: AsyncEngine = create_async_engine(str(config.POSTGRES_URI), echo=True)

# Session = sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)
# async_session_global = sessionmaker(
#     autocommit=False,
#     autoflush=False,
#     bind=engine,
#     class_=AsyncSession,
#     expire_on_commit=False,
# )

# async def get_async_session() -> AsyncGenerator[AsyncSession, Any]:
#     async with Session() as session:
#         yield session


async def create_db_and_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_maker() as session:
        yield session


async def get_user_db(session: AsyncSession = Depends(get_async_session)):
    yield SQLAlchemyUserDatabase(session, User, OAuthAccount)

async def get_access_token_db(
    session: AsyncSession = Depends(get_async_session),
):  
    yield SQLAlchemyAccessTokenDatabase(session, AccessToken)