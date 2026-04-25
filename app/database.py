import os
from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import (
    create_async_engine,
    async_sessionmaker,
    AsyncEngine,
    AsyncSession,
)

from app.config import settings
from app.models import Base


__engine: AsyncEngine = create_async_engine(url=settings.db_url, echo=settings.db_echo)
__sessionLocal: async_sessionmaker[AsyncSession] = async_sessionmaker(bind=__engine)


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with __sessionLocal() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()


def get_engine() -> AsyncEngine:
    """Get the database engine for direct access."""
    return __engine
