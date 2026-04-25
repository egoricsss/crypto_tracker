import logging

from app.client.client import CryptoAPIClient
from .repository import PriceRepository


logger = logging.getLogger(__name__)


class PriceSyncService:
    def __init__(
        self,
        api_client: CryptoAPIClient,
        repository: PriceRepository,
    ):
        self.api_client = api_client
        self.repository = repository
        self.tickers = ["btc_usdc", "eth_usdc"]

    async def sync_prices(self, tickers: list[str] | None = None) -> dict:
        """Основная бизнес-логика: fetch → upsert."""
        try:
            dtos = await self.api_client.fetch_price(
                tickers if tickers else self.tickers
            )
            logger.info(f"Fetched {len(dtos)} prices from Deribit")

            if not dtos:
                return {"fetched": 0, "upserted": 0, "status": "no_data"}

            upserted = await self.repository.upsert_prices(dtos)
            logger.info(f"Upserted {upserted} prices to database")

            return {"fetched": len(dtos), "upserted": upserted, "status": "success"}

        except Exception as e:
            logger.error(f"Sync failed: {e}", exc_info=True)
            raise
        finally:
            await self.api_client.close()
