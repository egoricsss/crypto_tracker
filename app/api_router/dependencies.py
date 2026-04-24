from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.price.repository import PriceRepository


async def get_price_repo(session: AsyncSession = Depends(get_db)) -> PriceRepository:
    return PriceRepository(session=session)


PriceRepoDep = Annotated[PriceRepository, Depends(get_price_repo)]
