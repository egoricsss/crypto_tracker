from decimal import Decimal
from datetime import datetime


from pydantic import BaseModel, field_validator, Field

from app.models import TickerEnum


class PriceDTO(BaseModel):
    ticker: TickerEnum
    current_price: Decimal
    time: datetime

    @field_validator("ticker", mode="before")
    @classmethod
    def normalize_ticker(cls, v: str) -> str:
        return v.lower() if isinstance(v, str) else v


class DeribitPriceResponse(BaseModel):
    jsonrpc: str = Field(..., pattern="^2\\.0$")
    result: dict[str, Decimal]
    id: int | None = None
    error: dict | None = None

    @field_validator("result", mode="before")
    @classmethod
    def convert_prices_to_decimal(cls, v: dict) -> dict:
        return {k: Decimal(str(v)) for k, v in v.items()}


class PriceCreateSchema(BaseModel):
    ticker: TickerEnum
    time: datetime
    current_price: Decimal


class PriceSchema(PriceCreateSchema):
    id: int
