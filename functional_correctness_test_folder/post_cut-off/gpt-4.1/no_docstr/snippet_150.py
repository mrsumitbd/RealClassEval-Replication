
from dataclasses import dataclass, field
from decimal import Decimal
from typing import Dict


@dataclass
class BudgetTracker:
    balance: Decimal = field(default=Decimal('0.00'))
    spent_by_agent: Dict[str, Decimal] = field(default_factory=dict)

    def can_afford(self, cost: Decimal) -> bool:
        return self.balance >= cost

    def spend(self, amount: Decimal, agent_card_name: str) -> None:
        if amount > self.balance:
            raise ValueError("Insufficient funds")
        self.balance -= amount
        if agent_card_name in self.spent_by_agent:
            self.spent_by_agent[agent_card_name] += amount
        else:
            self.spent_by_agent[agent_card_name] = amount
