from datetime import datetime, timezone
from decimal import Decimal
from enum import Enum

from sqlalchemy import Index, UniqueConstraint
from sqlalchemy.dialects.postgresql import ENUM, INTEGER, NUMERIC, TIMESTAMP
from sqlalchemy.orm import (DeclarativeBase, Mapped, declared_attr,
                            mapped_column)


class TickerEnum(Enum):
    BTC_USD = "btc_usdc"
    ETH_USD = "eth_usdc"


class Base(DeclarativeBase):
    @declared_attr
    def id(cls) -> Mapped[int]:
        return mapped_column(INTEGER, primary_key=True)


class Price(Base):
    __tablename__ = "prices"

    __table_args__ = (
        UniqueConstraint("ticker", "time", name="uq_prices_ticker_time"),
        Index(
            "ix_prices_ticker_time", "ticker", "time", postgresql_ops={"time": "DESC"}
        ),
    )

    ticker: Mapped[str] = mapped_column(ENUM(TickerEnum))
    time: Mapped[datetime] = mapped_column(
        TIMESTAMP(precision=3, timezone=True),
        nullable=False,
        default=lambda: datetime.now(timezone.utc),
    )
    current_price: Mapped[Decimal] = mapped_column(NUMERIC(20, 8), nullable=False)
