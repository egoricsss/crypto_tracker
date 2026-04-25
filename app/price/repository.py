from datetime import datetime, timezone

from sqlalchemy import and_, select
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.ext.asyncio import AsyncSession

from app.common.repositories import BaseRepository
from app.models import Price
from app.price.schemas import PriceCreateSchema


class PriceRepository(BaseRepository):
    def __init__(self, session: AsyncSession):
        self.session = session
        super().__init__(session=session, model=Price)

    async def upsert_prices(self, price_data: list[PriceCreateSchema]) -> int:
        stmt = insert(self.model).values([row.model_dump() for row in price_data])
        result = await self.session.execute(stmt)
        return result.rowcount

    async def get_latest_price_by_ticker(self, ticker: str) -> Price | None:
        stmt = (
            select(self.model)
            .where(self.model.ticker == ticker)
            .order_by(self.model.time.desc())
            .limit(1)
        )
        result = await self.session.scalar(stmt)
        return result

    async def get_latest_prices(self, tickers: list[str]) -> list[Price]:
        subq = (
            select(self.model.ticker, self.model.time)
            .where(self.model.ticker.in_([t.upper() for t in tickers]))
            .order_by(self.model.time.desc())
            .distinct(self.model.ticker)  # PostgreSQL-specific
        ).subquery()

        stmt = select(self.model).join(subq, self.model.time == subq.c.time)
        result = await self.session.scalars(stmt)
        return list(result.all())

    async def get_prices_by_date_range(
        self,
        ticker: str,
        start_date: datetime,
        end_date: datetime | None = None,
    ) -> list[Price]:
        end_date = end_date or datetime.now(timezone.utc)

        stmt = (
            select(self.model)
            .where(
                and_(
                    self.model.ticker == ticker,
                    self.model.time >= start_date,
                    self.model.time <= end_date,
                )
            )
            .order_by(self.model.time.desc())
        )
        result = await self.session.scalars(stmt)
        return result.all()
