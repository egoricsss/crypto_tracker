from app.client.client import CryptoAPIClient
from .repository import PriceRepository


class PriceSyncService:
    def __init__(
        self,
        api_client: CryptoAPIClient,
        repository: PriceRepository,
    ):
        self.api_client = api_client
        self.repository = repository

    async def sync(self, tickers: list[str]) -> dict:
        try:
            dtos = await self.api_client.fetch_prices(tickers)

            saved_count = await self.repository.upsert_prices(dtos)

        except Exception as e:
            ...
