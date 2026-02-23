import pytest
import pandas as pd
from ib_positions.client import IBDataFetcher


class DummyContract:
    def __init__(self):
        self.symbol = "AAPL"
        self.secType = "STK"
        self.primaryExchange = "NASDAQ"
        self.currency = "USD"
        self.lastTradeDateOrContractMonth = ""
        self.multiplier = ""


class DummyPortfolioItem:
    def __init__(self):
        self.contract = DummyContract()
        self.position = 10
        self.marketPrice = 150.0
        self.marketValue = 1500.0
        self.averageCost = 148.0


class DummyIB:
    def managedAccounts(self):
        return ["DU123"]

    def portfolio(self, account):
        return [DummyPortfolioItem()]


@pytest.mark.asyncio
async def test_fetch_positions_returns_dataframe():
    fetcher = IBDataFetcher()
    fetcher.ib = DummyIB()

    df = await fetcher.fetch_positions()

    assert isinstance(df, pd.DataFrame)
    assert not df.empty
    assert df.iloc[0]["symbol"] == "AAPL"
    assert df.iloc[0]["position"] == 10


def test_save_to_parquet(tmp_path):
    fetcher = IBDataFetcher()
    df = pd.DataFrame({
        "symbol": ["AAPL"],
        "date": ["2024-01-01"],
        "price": [150]
    })

    file_path = tmp_path / "test.parquet"
    fetcher.save_to_parquet(df, file_path)

    assert file_path.exists()