
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
    budget: Decimal = Decimal('0')
    spending: Dict[str, Decimal] = field(default_factory=dict)

    def can_afford(self, cost: Decimal) -> bool:
        return cost <= self.budget

    def spend(self, amount: Decimal, agent_card_name: str) -> None:
        if not self.can_afford(amount):
            raise ValueError("Insufficient budget")
        self.budget -= amount
        if agent_card_name in self.spending:
            self.spending[agent_card_name] += amount
        else:
            self.spending[agent_card_name] = amount
