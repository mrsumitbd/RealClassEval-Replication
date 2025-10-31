from dataclasses import dataclass, field
from decimal import Decimal, InvalidOperation
from datetime import datetime, timezone
from typing import Dict, List, Optional, Tuple


@dataclass
class BudgetTracker:
    '''
    Tracks agent spending and budget decisions.
    Provides comprehensive budget management including affordability checks,
    spending tracking per agent card, and cost analysis over time.
    '''
    total_budget: Optional[Decimal] = None

    remaining_budget: Decimal = field(init=False)
    total_spent: Decimal = field(init=False, default=Decimal("0"))
    per_card_spend: Dict[str, Decimal] = field(
        init=False, default_factory=dict)
    spend_history: List[Tuple[datetime, Decimal, str]
                        ] = field(init=False, default_factory=list)

    def __post_init__(self) -> None:
        self.total_budget = self._to_decimal(
            self.total_budget) if self.total_budget is not None else None
        self.remaining_budget = self.total_budget if self.total_budget is not None else Decimal(
            "Infinity")

    @staticmethod
    def _to_decimal(value: Optional[Decimal]) -> Decimal:
        if isinstance(value, Decimal):
            return +value
        if value is None:
            raise ValueError("Value cannot be None.")
        try:
            return +Decimal(str(value))
        except (InvalidOperation, ValueError, TypeError) as e:
            raise ValueError(f"Invalid decimal value: {value}") from e

    def can_afford(self, cost: Decimal) -> bool:
        '''Check if the agent can afford a given cost.'''
        amount = self._to_decimal(cost)
        if amount < 0:
            raise ValueError("Cost cannot be negative.")
        return self.remaining_budget >= amount

    def spend(self, amount: Decimal, agent_card_name: str) -> None:
        '''Record a spending transaction and update budget tracking.'''
        if not agent_card_name or not isinstance(agent_card_name, str):
            raise ValueError("agent_card_name must be a non-empty string.")
        amt = self._to_decimal(amount)
        if amt <= 0:
            raise ValueError("Spend amount must be greater than zero.")
        if not self.can_afford(amt):
            raise ValueError("Insufficient budget for this transaction.")

        self.remaining_budget -= amt
        self.total_spent += amt
        self.per_card_spend[agent_card_name] = self.per_card_spend.get(
            agent_card_name, Decimal("0")) + amt
        self.spend_history.append(
            (datetime.now(timezone.utc), amt, agent_card_name))
