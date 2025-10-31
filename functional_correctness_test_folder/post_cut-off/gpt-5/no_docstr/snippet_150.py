from dataclasses import dataclass, field
from decimal import Decimal
from typing import Dict


@dataclass
class BudgetTracker:
    total_budget: Decimal
    spent: Decimal = field(default=Decimal("0"))
    per_card_spend: Dict[str, Decimal] = field(default_factory=dict)

    def can_afford(self, cost: Decimal) -> bool:
        if cost is None:
            return False
        if not isinstance(cost, Decimal):
            try:
                cost = Decimal(cost)
            except Exception:
                return False
        if cost < 0:
            return False
        return self.total_budget - self.spent >= cost

    def spend(self, amount: Decimal, agent_card_name: str) -> None:
        if agent_card_name is None or not str(agent_card_name).strip():
            raise ValueError("agent_card_name must be a non-empty string")
        if not isinstance(amount, Decimal):
            try:
                amount = Decimal(amount)
            except Exception:
                raise ValueError(
                    "amount must be a Decimal or coercible to Decimal")
        if amount <= 0:
            raise ValueError("amount must be positive")
        if not self.can_afford(amount):
            raise ValueError("Insufficient budget to cover this expense")

        self.spent += amount
        self.per_card_spend[agent_card_name] = self.per_card_spend.get(
            agent_card_name, Decimal("0")) + amount
