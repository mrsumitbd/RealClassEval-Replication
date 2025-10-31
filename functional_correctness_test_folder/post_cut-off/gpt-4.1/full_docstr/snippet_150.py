
from dataclasses import dataclass, field
from decimal import Decimal
from typing import Dict, List, Tuple


@dataclass
class BudgetTracker:
    '''
    Tracks agent spending and budget decisions.
    Provides comprehensive budget management including affordability checks,
    spending tracking per agent card, and cost analysis over time.
    '''
    total_budget: Decimal
    spent: Decimal = Decimal('0.00')
    transactions: List[Tuple[str, Decimal]] = field(default_factory=list)
    per_card_spending: Dict[str, Decimal] = field(default_factory=dict)

    def can_afford(self, cost: Decimal) -> bool:
        '''Check if the agent can afford a given cost.'''
        return self.spent + cost <= self.total_budget

    def spend(self, amount: Decimal, agent_card_name: str) -> None:
        '''Record a spending transaction and update budget tracking.'''
        if not self.can_afford(amount):
            raise ValueError("Insufficient budget for this transaction.")
        self.spent += amount
        self.transactions.append((agent_card_name, amount))
        if agent_card_name in self.per_card_spending:
            self.per_card_spending[agent_card_name] += amount
        else:
            self.per_card_spending[agent_card_name] = amount
