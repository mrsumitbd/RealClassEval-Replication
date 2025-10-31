
from dataclasses import dataclass
from decimal import Decimal


@dataclass
class BudgetTracker:
    '''
    Tracks agent spending and budget decisions.
    Provides comprehensive budget management including affordability checks,
    spending tracking per agent card, and cost analysis over time.
    '''
    budget: Decimal = Decimal('0.0')
    spending_records: dict = None  # type: ignore

    def __post_init__(self) -> None:
        if self.spending_records is None:
            self.spending_records = {}

    def can_afford(self, cost: Decimal) -> bool:
        '''Check if the agent can afford a given cost.'''
        return self.budget >= cost

    def spend(self, amount: Decimal, agent_card_name: str) -> None:
        '''Record a spending transaction and update budget tracking.'''
        if not self.can_afford(amount):
            raise ValueError("Insufficient budget for this transaction.")
        self.budget -= amount
        if agent_card_name not in self.spending_records:
            self.spending_records[agent_card_name] = Decimal('0.0')
        self.spending_records[agent_card_name] += amount
