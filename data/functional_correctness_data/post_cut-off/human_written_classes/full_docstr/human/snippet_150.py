from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass
from decimal import Decimal

@dataclass
class BudgetTracker:
    """
    Tracks agent spending and budget decisions.

    Provides comprehensive budget management including affordability checks,
    spending tracking per agent card, and cost analysis over time.
    """
    initial_budget: Decimal
    current_balance: Decimal
    total_spent: Decimal
    spending_per_agent_card: Dict[str, Decimal]
    evaluations_count: int
    average_cost_per_eval: Decimal

    def can_afford(self, cost: Decimal) -> bool:
        """Check if the agent can afford a given cost."""
        return self.current_balance >= cost

    def spend(self, amount: Decimal, agent_card_name: str) -> None:
        """Record a spending transaction and update budget tracking."""
        self.current_balance -= amount
        self.total_spent += amount
        self.spending_per_agent_card[agent_card_name] = self.spending_per_agent_card.get(agent_card_name, Decimal('0')) + amount
        self.evaluations_count += 1
        if self.evaluations_count > 0:
            self.average_cost_per_eval = self.total_spent / self.evaluations_count