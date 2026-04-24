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


async def init_db() -> None:
    with __engine.begin() as conn:
        from app.models import Price

        await conn.run_sync(Base.metadata.create_all)


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
