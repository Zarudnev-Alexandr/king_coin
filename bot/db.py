import os
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql+asyncpg://postgres:test@db:5432/king_coin")

engine = create_async_engine(url=str(DATABASE_URL), echo=True)
async_session = async_sessionmaker(engine, expire_on_commit=False)


async def get_db() -> AsyncSession:
    return async_session()
