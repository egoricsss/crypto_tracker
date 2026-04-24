from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.dialects.postgresql import insert

from app.models import Price
from .schemas import PriceDTO


class PriceRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    # return saved rows count
    async def upsert_prices(self, dtos: list[PriceDTO]) -> int: ...
