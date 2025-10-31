
from dataclasses import dataclass, field
from decimal import Decimal
from typing import Dict


@dataclass
class BudgetTracker:
    '''
    Tracks agent spending and budget decisions.
    Provides comprehensive budget management including affordability checks,
    spending tracking per agent card, and cost analysis over time.
    '''
    budget: Decimal = field(default_factory=Decimal)
    spent: Dict[str, Decimal] = field(default_factory=dict)

    def can_afford(self, cost: Decimal) -> bool:
        return self.budget >= cost

    def spend(self, amount: Decimal, agent_card_name: str) -> None:
        if self.can_afford(amount):
            self.budget -= amount
            if agent_card_name in self.spent:
                self.spent[agent_card_name] += amount
            else:
                self.spent[agent_card_name] = amount
        else:
            raise ValueError("Insufficient budget to cover the cost.")
