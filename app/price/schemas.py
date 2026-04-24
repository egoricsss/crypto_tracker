from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel

from app.models import TickerEnum


class PriceSchema(BaseModel):
    id: int
    ticker: TickerEnum
    time: datetime
    current_price: Decimal
