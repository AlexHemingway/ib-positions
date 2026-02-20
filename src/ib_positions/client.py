import asyncio
import logging
import pandas as pd
from ib_async import IB, Contract, util
from .models import Position

# Set up basic logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class IBDataFetcher:
    """
    Async wrapper for fetching portfolio positions and historical prices from Interactive Brokers using ib_async.
    """

    def __init__(self):
        # Initialize IB client
        self.ib = IB()
        # Delay between requests to avoid hitting IB API rate limits
        self.REQUEST_DELAY = 0.4

    async def fetch_positions(self) -> pd.DataFrame:
        """
        Fetch current positions from IB and return as a DataFrame.
        """
        account = self.ib.managedAccounts()[0]
        portfolio = self.ib.portfolio(account)

        results = []
        for item in portfolio:
            results.append({
                'symbol': item.contract.symbol,
                'contractType': item.contract.secType,
                'exchange': item.contract.primaryExchange,
                'currency': item.contract.currency,
                'lastTradeDate': item.contract.lastTradeDateOrContractMonth,
                'multiplier': item.contract.multiplier,
                'position': item.position,
                'marketPrice': item.marketPrice,
                'marketValue': item.marketValue,
                'avgCost': item.averageCost,
            })

        return pd.DataFrame(results)

    async def fetch_hist_prices(
        self,
        symbol: str,
        sec_type: str,
        exchange: str,
        currency: str,
        last_trade_date: str = '',
        multiplier: str = '',
        duration: str = '5 Y',
        bar_size: str = '1 day'
    ) -> pd.DataFrame:
        """
        Fetch historical price data for a single contract.

        Returns:
            pd.DataFrame: historical bars with symbol and lastTradeDate columns.
        """
        # Build contract
        contract_kwargs = {
            'symbol': symbol,
            'secType': sec_type,
            'exchange': exchange or 'SMART',
            'currency': currency
        }

        if sec_type in ('FUT', 'CONTFUT'):
            contract_kwargs['lastTradeDateOrContractMonth'] = last_trade_date
            if multiplier:
                contract_kwargs['multiplier'] = multiplier

        contract = Contract(**contract_kwargs)

        # Qualify contract with IB
        try:
            await self.ib.qualifyContractsAsync(contract)
        except Exception as e:
            logger.error(f"Error qualifying contract for [{symbol} {last_trade_date}]: {e}")
            return None

        # Fetch historical data
        try:
            bars = await self.ib.reqHistoricalDataAsync(
                contract,
                endDateTime='',
                durationStr=duration,
                barSizeSetting=bar_size,
                whatToShow='TRADES',
                useRTH=True,
                formatDate=1,
                timeout=10
            )
        except Exception as e:
            logger.error(f"Error fetching historical data for [{symbol} {last_trade_date}]: {e}")
            return None

        if not bars:
            logger.warning(f"No historical data returned for [{symbol} {last_trade_date}]")
            return None

        df = util.df(bars)
        df['symbol'] = symbol
        df['lastTradeDate'] = last_trade_date
        return df

    async def fetch_hist_for_positions(self, duration: str, bar_size: str) -> pd.DataFrame:
        """
        Fetch historical price data for all positions in the current portfolio.

        Loops over each position, fetches data, adds pacing delay to avoid rate limits,
        and combines results into a single DataFrame.
        """
        positions_df = await self.fetch_positions()
        if positions_df.empty:
            logger.warning("No positions found in portfolio.")
            return pd.DataFrame()

        frames: list[pd.DataFrame] = []

        for _, row in positions_df.iterrows():
            df = await self.fetch_hist_prices(
                symbol=row['symbol'],
                sec_type=row['contractType'],
                exchange=row['exchange'],
                currency=row['currency'],
                last_trade_date=row.get('lastTradeDate', ''),
                multiplier=row.get('multiplier', ''),
                duration=duration,
                bar_size=bar_size
            )
            if df is not None:
                df['position'] = row['position']
                df['marketValue'] = row['marketValue']
                df['avgCost'] = row['avgCost']
                frames.append(df)

            # Delay to respect rate limits
            await asyncio.sleep(self.REQUEST_DELAY)

        if not frames:
            logger.warning("No historical data fetched for any positions.")
            return pd.DataFrame()

        combined_df = pd.concat(frames, ignore_index=True)
        logger.info(f"Retrieved {len(combined_df)} bars across {combined_df['symbol'].nunique()} symbols")
        return combined_df

    def save_to_parquet(self, df: pd.DataFrame, filename: str):
        """
        Save DataFrame to Parquet file (compressed, partitioned by symbol).
        """
        if df.empty:
            logger.warning("Empty DataFrame - nothing to save")
            return
        
        df.to_parquet(filename,
                      compression='snappy',
                      index=False,
                      partition_cols=['symbol'])
        
        logger.info(f"Saved {len(df)} rows to {filename}")