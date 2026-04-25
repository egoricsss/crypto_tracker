import logging

from celery import shared_task
from sqlalchemy.ext.asyncio import AsyncSession

from app.config import settings
from app.database import get_engine
from app.price.client import CryptoAPIClient
from app.price.repository import PriceRepository
from app.price.service import PriceSyncService

logger = logging.getLogger(__name__)


@shared_task(bind=True, max_retries=3)
def fetch_deribit_prices(self, tickers: list[str] | None = None):
    """
    Celery task для сбора данных с Deribit биржи.
    Запускается каждую минуту через celery-beat.

    Args:
        tickers: Список тикеров для сбора (по умолчанию ["btc_usdc", "eth_usdc"])
    """
    import asyncio

    async def _run_sync():
        # Создаем асинхронный клиент
        api_client = CryptoAPIClient(base_url=settings.base_url, timeout=30.0)

        # Создаем сессию базы данных напрямую из engine
        engine = get_engine()
        async with engine.begin() as session:
            try:
                # Создаем репозиторий и сервис
                repository = PriceRepository(session=session)
                service = PriceSyncService(api_client=api_client, repository=repository)

                # Выполняем синхронизацию цен
                result = await service.sync_prices(tickers)
                logger.info(f"Price sync completed: {result}")
                return result

            except Exception as exc:
                logger.error(f"Price sync failed: {exc}", exc_info=True)
                raise self.retry(exc=exc, countdown=60)  # Retry through 1 minute

    # Запускаем асинхронный код в синхронном контексте Celery
    return asyncio.run(_run_sync())
