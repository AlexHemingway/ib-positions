import asyncio
from src.ib_positions.client import IBDataFetcher
from ib_async import IB

async def main():
    # Connect to IB API
    ib = IB()
    await ib.connectAsync(host='127.0.0.1', port=4001, clientId=1)

    fetcher = IBDataFetcher()
    fetcher.ib = ib

    # Fetch historical prices for all positions
    df = await fetcher.fetch_hist_for_positions(duration="1 M", bar_size="1 day")
    print(df.head())

    # Save results
    fetcher.save_to_parquet(df, 'test_git.parquet')

    # Disconnect IB
    ib.disconnect()
    print('Disconnected from IB API')

if __name__ == "__main__":
    asyncio.run(main())