
from dataclasses import dataclass
from decimal import Decimal


@dataclass
class BudgetTracker:
    '''
    Tracks agent spending and budget decisions.
    Provides comprehensive budget management including affordability checks,
    spending tracking per agent card, and cost analysis over time.
    '''
    budget: Decimal = Decimal('0')
    spending: dict[str, Decimal] = None

    def __post_init__(self):
        if self.spending is None:
            self.spending = {}

    def can_afford(self, cost: Decimal) -> bool:
        return self.budget >= cost

    def spend(self, amount: Decimal, agent_card_name: str) -> None:
        if self.can_afford(amount):
            self.budget -= amount
            if agent_card_name in self.spending:
                self.spending[agent_card_name] += amount
            else:
                self.spending[agent_card_name] = amount
