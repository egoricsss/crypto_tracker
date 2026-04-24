from typing import Generic, Optional, Type, TypeVar

from sqlalchemy import delete, insert, select, update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import DeclarativeBase

T = TypeVar("T", bound=DeclarativeBase)


class BaseRepository(Generic[T]):
    def __init__(self, session: AsyncSession, model: Type[T]):
        self.session = session
        self.model = model

    async def get_all(self) -> list[T]:
        result = await self.session.scalars(
            select(self.model).order_by(self.model.id.desc())
        )
        return result.all()

    async def get_by_id(self, obj_id: int) -> Optional[T]:
        return await self.session.scalar(
            select(self.model).where(self.model.id == obj_id)
        )

    async def get_with_filters(self, **kwargs) -> list[T]:
        stmt = select(self.model).filter_by(**kwargs).order_by(self.model.id.desc())
        result = await self.session.scalars(stmt)
        return result.all()

    async def create(self, **kwargs) -> T:
        stmt = insert(self.model).values(**kwargs).returning(self.model)
        return await self.session.scalar(stmt)

    async def update(self, obj_id: int, **kwargs) -> T:
        stmt = (
            update(self.model)
            .where(self.model.id == obj_id)
            .values(**kwargs)
            .returning(self.model)
        )
        return await self.session.scalar(stmt)

    async def delete(self, obj_id: int) -> bool:
        stmt = delete(self.model).where(self.model.id == obj_id)
        result = await self.session.execute(stmt)
        return result.rowcount > 0

    async def delete_all(self) -> bool:
        stmt = delete(self.model)
        result = await self.session.execute(stmt)
        return result.rowcount > 0
