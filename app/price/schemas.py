from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel

from app.models import TickerEnum


class PriceCreateSchema(BaseModel):
    ticker: TickerEnum
    time: datetime
    current_price: Decimal


class PriceSchema(PriceCreateSchema):
    id: int
