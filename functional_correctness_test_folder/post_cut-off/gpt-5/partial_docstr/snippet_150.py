from dataclasses import dataclass, field
from datetime import datetime, timezone
from decimal import Decimal, ROUND_HALF_UP
from typing import Dict, List, Optional, Tuple


@dataclass
class BudgetTracker:
    '''
    Tracks agent spending and budget decisions.
    Provides comprehensive budget management including affordability checks,
    spending tracking per agent card, and cost analysis over time.
    '''
    total_budget: Optional[Decimal] = None
    spent_total: Decimal = field(default_factory=lambda: Decimal("0"))
    per_card_spend: Dict[str, Decimal] = field(default_factory=dict)
    transactions: List[Tuple[datetime, str, Decimal]
                       ] = field(default_factory=list)
    precision: Decimal = Decimal("0.01")

    def _normalize_amount(self, amount: Decimal) -> Decimal:
        if not isinstance(amount, Decimal):
            amount = Decimal(str(amount))
        if amount.is_nan() or amount.is_infinite():
            raise ValueError("Amount must be a finite number.")
        q = self.precision
        if q <= 0:
            raise ValueError("Precision must be a positive Decimal.")
        return amount.quantize(q, rounding=ROUND_HALF_UP)

    @property
    def remaining_budget(self) -> Optional[Decimal]:
        if self.total_budget is None:
            return None
        remaining = self.total_budget - self.spent_total
        return self._normalize_amount(remaining)

    def can_afford(self, cost: Decimal) -> bool:
        cost = self._normalize_amount(cost)
        if cost < 0:
            raise ValueError("Cost cannot be negative.")
        if self.total_budget is None:
            return True
        return cost <= (self.total_budget - self.spent_total)

    def spend(self, amount: Decimal, agent_card_name: str) -> None:
        amount = self._normalize_amount(amount)
        if amount < 0:
            raise ValueError("Spend amount cannot be negative.")
        if not agent_card_name or not isinstance(agent_card_name, str):
            raise ValueError("agent_card_name must be a non-empty string.")
        if amount == 0:
            # No-op but still record for traceability if desired; here we ignore
            return
        if not self.can_afford(amount):
            remaining = self.remaining_budget
            if remaining is None:
                remaining_str = "unlimited"
            else:
                remaining_str = str(self._normalize_amount(remaining))
            raise ValueError(
                f"Insufficient budget: attempted {amount}, remaining {remaining_str}.")

        self.spent_total = self._normalize_amount(self.spent_total + amount)
        self.per_card_spend[agent_card_name] = self._normalize_amount(
            self.per_card_spend.get(agent_card_name, Decimal("0")) + amount
        )
        self.transactions.append(
            (datetime.now(timezone.utc), agent_card_name, amount))
