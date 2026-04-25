from typing import Annotated, AsyncGenerator

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.price.repository import PriceRepository
from app.price.client import CryptoAPIClient
from app.price.service import PriceSyncService
from app.config import settings


async def get_price_repo(session: AsyncSession = Depends(get_db)) -> PriceRepository:
    return PriceRepository(session=session)


async def get_price_service(
    repository: PriceRepository = Depends(get_price_repo),
) -> AsyncGenerator[PriceSyncService, None]:
    client = CryptoAPIClient(base_url=settings.base_url)
    yield PriceSyncService(api_client=client, repository=repository)
    await client.close()


PriceRepoDep = Annotated[PriceRepository, Depends(get_price_repo)]
PriceSyncServiceDep = Annotated[PriceSyncService, Depends(get_price_service)]
