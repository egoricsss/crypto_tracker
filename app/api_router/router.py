from datetime import datetime

from fastapi import APIRouter, HTTPException, status

from app.price.schemas import PriceSchema
from app.models import TickerEnum
from .dependencies import PriceRepoDep, PriceSyncServiceDep

router = APIRouter()


@router.get("/prices/fetch")
async def get_price(price_service: PriceSyncServiceDep) -> int:
    inserted_rows = await price_service.sync()
    return inserted_rows


@router.get("/prices/latest", response_model=PriceSchema)
async def get_latest_prices(repository: PriceRepoDep, ticker: TickerEnum):
    latest_price = await repository.get_latest_price_by_ticker(ticker=ticker)
    if latest_price is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="database is empty"
        )
    return latest_price


@router.get("/prices/range_by_time", response_model=list[PriceSchema])
async def get_prices_by_time_range(
    repository: PriceRepoDep,
    ticker: TickerEnum,
    start_date: datetime,
    end_date: datetime | None = None,
):
    ranged_prices = await repository.get_prices_by_date_range(
        ticker=ticker, start_date=start_date, end_date=end_date
    )
    return ranged_prices


@router.get("/prices", response_model=list[PriceSchema])
async def get_all_prices(repository: PriceRepoDep, ticker: TickerEnum | None = None):
    if ticker is None:
        all_prices = await repository.get_all()
    else:        
        all_prices = await repository.get_with_filters(ticker=ticker)
    return all_prices
