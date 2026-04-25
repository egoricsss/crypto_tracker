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
        self.tickers = ["btc_usdc", "eth_usdc"]

    async def sync(self) -> int:
        try:
            prices_dto = await self.api_client.fetch_price(self.tickers)

            result = await self.repository.upsert_prices(prices_dto)

            return result

        except Exception as e:
            print(f"Error: {e}")
            return 0
