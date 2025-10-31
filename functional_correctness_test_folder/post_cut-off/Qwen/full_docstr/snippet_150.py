
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
    spending: Dict[str, Decimal] = field(default_factory=dict)

    def can_afford(self, cost: Decimal) -> bool:
        '''Check if the agent can afford a given cost.'''
        return self.budget >= cost

    def spend(self, amount: Decimal, agent_card_name: str) -> None:
        '''Record a spending transaction and update budget tracking.'''
        if self.can_afford(amount):
            self.budget -= amount
            if agent_card_name in self.spending:
                self.spending[agent_card_name] += amount
            else:
                self.spending[agent_card_name] = amount
        else:
            raise ValueError("Insufficient funds to complete the transaction.")
