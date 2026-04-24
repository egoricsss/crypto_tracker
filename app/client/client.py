import aiohttp
from tenacity import (
    retry,
    stop_after_attempt,
    wait_exponential,
    retry_if_exception_type,
)

from .schemas import PriceDTO


class CryptoAPIClient:
    def __init__(
        self, base_url: str, api_key: str | None = None, timeout: float = 10.0
    ):
        self.base_url = base_url
        self.api_key = api_key
        self.timeout = timeout
        self.headers = {"Authorization": f"Bearer {api_key}"} if api_key else {}
        self._session: aiohttp.ClientSession | None = None

    async def _ensure_session(self) -> aiohttp.ClientSession:
        if self._session is None or self._session.closed:
            self._session = aiohttp.ClientSession(
                timeout=self.timeout, headers=self.headers
            )
        return self._session

    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=2, max=10),
        retry=retry_if_exception_type((aiohttp.ClientError, TimeoutError)),
        reraise=True,
    )
    async def fetch_price(self, tickers: list[str]) -> list[PriceDTO]:
        session = await self._ensure_session()
        params = None

        async with session.get(f"{self.base_url}/prices", params=params) as response:
            response.raise_for_status()
            raw_data = await response.json()
            # todo: create reponse foe Deribit API
            ...

            return PriceDTO(...)

    async def close(self):
        if self._session and not self._session.closed:
            await self._session.close()
