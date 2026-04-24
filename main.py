import asyncio

from app.client import CryptoAPIClient


async def main():
    client = CryptoAPIClient(base_url="https://test.deribit.com/api/v2/")
    try:
        fetched_data = await client.fetch_price(["btc_usdc", "eth_usdc"])
        print(*fetched_data, sep="\n")
    finally:
        await client.close()


if __name__ == "__main__":
    asyncio.run(main())
