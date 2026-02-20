from pydantic import BaseModel
from typing import Optional

class Position(BaseModel):
    """
    Represents a position in a portfolio.
    Stores contract info, quantity, and pricing details.
    """
    symbol: str
    contractType: str
    exchange: str
    currency: str
    lastTradeDate: Optional[str] = ''
    multiplier: Optional[str] = ''
    position: float
    marketPrice: Optional[float] = None
    marketValue: Optional[float] = None
    avgCost: Optional[float] = None

# Optional: Could add a MarketPrice model if you want to store historical snapshot separately
class MarketPrice(BaseModel):
    """
    Represents a market price snapshot for a single contract.
    """
    conid: int
    bid: Optional[float] = None
    ask: Optional[float] = None
    last: Optional[float] = None