from dataclasses import dataclass, field
from decimal import Decimal
from typing import Dict, List


@dataclass
class BudgetTracker:
    '''
    Tracks agent spending and budget decisions.
    Provides comprehensive budget management including affordability checks,
    spending tracking per agent card, and cost analysis over time.
    '''
    total_budget: Decimal
    spent: Decimal = Decimal('0.0')
    spending_history: List[Dict] = field(default_factory=list)
    card_spending: Dict[str, Decimal] = field(default_factory=dict)

    def can_afford(self, cost: Decimal) -> bool:
        '''Check if the agent can afford a given cost.'''
        return self.spent + cost <= self.total_budget

    def spend(self, amount: Decimal, agent_card_name: str) -> None:
        '''Record a spending transaction and update budget tracking.'''
        if not self.can_afford(amount):
            raise ValueError("Insufficient budget to spend this amount.")
        self.spent += amount
        self.card_spending[agent_card_name] = self.card_spending.get(
            agent_card_name, Decimal('0.0')) + amount
        self.spending_history.append({
            'amount': amount,
            'agent_card_name': agent_card_name
        })
