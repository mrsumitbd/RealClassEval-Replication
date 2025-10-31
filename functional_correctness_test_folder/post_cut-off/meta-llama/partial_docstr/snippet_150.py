
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
    total_budget: Decimal
    agent_spendings: Dict[str, Decimal] = field(default_factory=dict)

    def can_afford(self, cost: Decimal) -> bool:
        return self.total_budget >= cost

    def spend(self, amount: Decimal, agent_card_name: str) -> None:
        if not self.can_afford(amount):
            raise ValueError("Insufficient budget")

        self.total_budget -= amount
        self.agent_spendings[agent_card_name] = self.agent_spendings.get(
            agent_card_name, Decimal(0)) + amount
