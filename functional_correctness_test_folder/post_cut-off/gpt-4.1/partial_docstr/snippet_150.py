
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
    total_budget: Decimal = Decimal('0.00')
    spent: Decimal = Decimal('0.00')
    spending_history: List[Tuple[str, Decimal]] = field(default_factory=list)
    agent_card_spending: Dict[str, Decimal] = field(default_factory=dict)

    def can_afford(self, cost: Decimal) -> bool:
        return (self.total_budget - self.spent) >= cost

    def spend(self, amount: Decimal, agent_card_name: str) -> None:
        if not self.can_afford(amount):
            raise ValueError("Insufficient budget to spend this amount.")
        self.spent += amount
        self.spending_history.append((agent_card_name, amount))
        if agent_card_name in self.agent_card_spending:
            self.agent_card_spending[agent_card_name] += amount
        else:
            self.agent_card_spending[agent_card_name] = amount
