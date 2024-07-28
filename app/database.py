from asyncio import current_task
from typing import AsyncIterator

import asyncpg
from marshmallow.exceptions import SCHEMA
from sqlalchemy import text
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncEngine, async_scoped_session
from sqlalchemy.ext.asyncio import AsyncSession
import os

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql+asyncpg://postgres:test@db:5432/king_coin")

# async def init_db():
#     pool = await asyncpg.create_pool(DATABASE_URL)
#     engine = create_async_engine(
#         url=str(DATABASE_URL),
#         pool_size=20,
#         max_overflow=10,
#         echo=True,
#         creator=pool.acquire  # используем creator, чтобы использовать пул от asyncpg
#     )
#     async_session = async_sessionmaker(engine, expire_on_commit=False)
#     return async_session
#
# async_session = None
#
# async def get_db() -> AsyncSession:
#     async with async_session() as session:
#         yield session


class DatabaseSessionManager:
    def __init__(self):
        self.engine: AsyncEngine | None = None
        self.session_maker = None
        self.session = None

    def init_db(self):
        # Database connection parameters...

        # Creating an asynchronous engine
        self.engine = create_async_engine(
            DATABASE_URL, pool_size=20, max_overflow=0, pool_pre_ping=False
        )

        # Creating an asynchronous session class
        self.session_maker = async_sessionmaker(
            autocommit=False, autoflush=False, bind=self.engine
        )

        # Creating a scoped session
        self.session = async_scoped_session(self.session_maker, scopefunc=current_task)

    async def close(self):
        # Closing the database session...
        if self.engine is None:
            raise Exception("DatabaseSessionManager is not initialized")
        await self.engine.dispose()


sessionmanager = DatabaseSessionManager()


async def get_db() -> AsyncIterator[AsyncSession]:
    session = sessionmanager.session()
    if session is None:
        raise Exception("DatabaseSessionManager is not initialized")
    try:
        # Setting the search path and yielding the session...
        yield session
    except Exception:
        await session.rollback()
        raise
    finally:
        # Closing the session after use...
        await session.close()