
from dataclasses import dataclass, field
from decimal import Decimal
from typing import Dict, List
from datetime import datetime


@dataclass
class BudgetTracker:
    '''
    Tracks agent spending and budget decisions.
    Provides comprehensive budget management including affordability checks,
    spending tracking per agent card, and cost analysis over time.
    '''
    total_budget: Decimal
    current_balance: Decimal = field(init=False)
    spending_history: List[Dict] = field(default_factory=list)
    agent_spending: Dict[str, Decimal] = field(default_factory=dict)

    def __post_init__(self):
        self.current_balance = self.total_budget

    def can_afford(self, cost: Decimal) -> bool:
        '''Check if the agent can afford a given cost.'''
        return self.current_balance >= cost

    def spend(self, amount: Decimal, agent_card_name: str) -> None:
        '''Record a spending transaction and update budget tracking.'''
        if not self.can_afford(amount):
            raise ValueError(f"Insufficient funds to spend {amount}")

        self.current_balance -= amount
        self.spending_history.append({
            'amount': amount,
            'agent_card_name': agent_card_name,
            'timestamp': datetime.now()
        })

        if agent_card_name in self.agent_spending:
            self.agent_spending[agent_card_name] += amount
        else:
            self.agent_spending[agent_card_name] = amount
