from dataclasses import dataclass, field
from datetime import datetime, date, timezone
from decimal import Decimal, ROUND_HALF_UP
from typing import Dict, List, Tuple, Optional


@dataclass
class BudgetTracker:
    """
    Tracks agent spending and budget decisions.
    Provides comprehensive budget management including affordability checks,
    spending tracking per agent card, and cost analysis over time.
    """
    total_budget: Decimal
    hard_limit: bool = True
    currency_scale: int = 2

    spent_total: Decimal = field(default=Decimal("0"))
    spent_by_card: Dict[str, Decimal] = field(default_factory=dict)
    spent_by_day: Dict[date, Decimal] = field(default_factory=dict)
    transactions: List[Tuple[datetime, Decimal, str]
                       ] = field(default_factory=list)
    last_spent_at: Optional[datetime] = None

    _quantize_unit: Decimal = field(init=False, repr=False)

    def __post_init__(self) -> None:
        self._quantize_unit = Decimal("1").scaleb(-self.currency_scale)
        self.total_budget = self._q(self.total_budget)
        self.spent_total = self._q(self.spent_total)
        if self.total_budget < Decimal("0"):
            raise ValueError("total_budget cannot be negative")
        if self.spent_total < Decimal("0"):
            raise ValueError("spent_total cannot be negative")
        if self.spent_total > self.total_budget and self.hard_limit:
            raise ValueError(
                "initial spent_total exceeds total_budget under hard limit")

    @property
    def remaining_budget(self) -> Decimal:
        return self._q(self.total_budget - self.spent_total)

    def can_afford(self, cost: Decimal) -> bool:
        """Check if the agent can afford a given cost."""
        c = self._q(cost)
        if c < Decimal("0"):
            c = Decimal("0")
        return self.remaining_budget >= c

    def spend(self, amount: Decimal, agent_card_name: str) -> None:
        """Record a spending transaction and update budget tracking."""
        if not agent_card_name or not agent_card_name.strip():
            raise ValueError("agent_card_name must be a non-empty string")

        amt = self._q(amount)
        if amt <= Decimal("0"):
            raise ValueError("amount must be positive")

        if self.hard_limit and not self.can_afford(amt):
            raise ValueError(
                "insufficient budget for this spend under hard limit")

        self.spent_total = self._q(self.spent_total + amt)

        prev_card_total = self.spent_by_card.get(agent_card_name, Decimal("0"))
        self.spent_by_card[agent_card_name] = self._q(prev_card_total + amt)

        today = datetime.now(timezone.utc).date()
        self.spent_by_day[today] = self._q(
            self.spent_by_day.get(today, Decimal("0")) + amt)

        now = datetime.now(timezone.utc)
        self.transactions.append((now, amt, agent_card_name))
        self.last_spent_at = now

    def _q(self, amount: Decimal) -> Decimal:
        if not isinstance(amount, Decimal):
            amount = Decimal(amount)
        return amount.quantize(self._quantize_unit, rounding=ROUND_HALF_UP)
