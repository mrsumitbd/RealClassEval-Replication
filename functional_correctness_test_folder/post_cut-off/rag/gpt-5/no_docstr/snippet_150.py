from dataclasses import dataclass, field
from decimal import Decimal
from datetime import datetime, timezone
from typing import Dict, List, Any


@dataclass
class BudgetTracker:
    '''
    Tracks agent spending and budget decisions.
    Provides comprehensive budget management including affordability checks,
    spending tracking per agent card, and cost analysis over time.
    '''
    budget_limit: Decimal = Decimal('0')
    remaining_budget: Decimal = field(init=False)
    total_spent: Decimal = field(init=False, default=Decimal('0'))
    spend_by_card: Dict[str, Decimal] = field(default_factory=dict)
    transactions: List[Dict[str, Any]] = field(default_factory=list)

    def __post_init__(self) -> None:
        if not isinstance(self.budget_limit, Decimal):
            self.budget_limit = Decimal(self.budget_limit)
        self.remaining_budget = self.budget_limit

    def can_afford(self, cost: Decimal) -> bool:
        '''Check if the agent can afford a given cost.'''
        if not isinstance(cost, Decimal):
            cost = Decimal(cost)
        if cost.is_nan() or cost < 0:
            raise ValueError('Cost must be a non-negative Decimal.')
        return cost <= self.remaining_budget

    def spend(self, amount: Decimal, agent_card_name: str) -> None:
        '''Record a spending transaction and update budget tracking.'''
        if not isinstance(amount, Decimal):
            amount = Decimal(amount)
        if amount.is_nan() or amount < 0:
            raise ValueError('Amount must be a non-negative Decimal.')
        if not agent_card_name:
            raise ValueError('agent_card_name must be a non-empty string.')
        if not self.can_afford(amount):
            raise ValueError('Insufficient budget for this transaction.')

        self.remaining_budget -= amount
        self.total_spent += amount
        self.spend_by_card[agent_card_name] = self.spend_by_card.get(
            agent_card_name, Decimal('0')) + amount
        self.transactions.append(
            {
                'timestamp': datetime.now(timezone.utc).isoformat(),
                'agent_card_name': agent_card_name,
                'amount': amount,
                'remaining_budget': self.remaining_budget,
            }
        )
