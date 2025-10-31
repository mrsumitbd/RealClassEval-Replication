
from dataclasses import dataclass, field
from decimal import Decimal
from typing import Dict


@dataclass
class BudgetTracker:
    budget: Decimal = field(default_factory=lambda: Decimal('0.00'))
    expenses: Dict[str, Decimal] = field(default_factory=dict)

    def can_afford(self, cost: Decimal) -> bool:
        return self.budget >= cost

    def spend(self, amount: Decimal, agent_card_name: str) -> None:
        if self.can_afford(amount):
            self.budget -= amount
            if agent_card_name in self.expenses:
                self.expenses[agent_card_name] += amount
            else:
                self.expenses[agent_card_name] = amount
        else:
            raise ValueError("Insufficient funds")
