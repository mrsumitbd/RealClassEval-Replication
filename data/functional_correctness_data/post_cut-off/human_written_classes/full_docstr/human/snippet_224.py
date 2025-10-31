from typing import Any, Dict, List, Optional
from dataclasses import dataclass, field
import pandas as pd

@dataclass
class TradeRecord:
    """Canonical representation of a single fill/order execution."""
    timestamp: pd.Timestamp
    symbol: str
    action: str
    quantity: float
    price: float
    strategy_id: Optional[str] = None
    commission: float = 0.0
    fees: float = 0.0
    metadata: Dict[str, Any] = field(default_factory=dict)

    @property
    def value(self) -> float:
        """Absolute dollar value of the fill (signed)."""
        sign = 1 if self.action.lower() == 'buy' else -1
        return sign * self.quantity * self.price

    @property
    def realized_pnl(self) -> float:
        """Realized P&L for this trade (simplified calculation)."""
        if self.action.lower() == 'sell':
            return self.quantity * self.price - self.commission - self.fees
        else:
            return 0.0