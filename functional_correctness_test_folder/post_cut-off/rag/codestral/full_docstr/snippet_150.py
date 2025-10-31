
from dataclasses import dataclass, field
from decimal import Decimal
from typing import Dict, List, Optional


@dataclass
class BudgetTracker:
    """
    Tracks agent spending and budget decisions.
    Provides comprehensive budget management including affordability checks,
    spending tracking per agent card, and cost analysis over time.
    """
    budget: Decimal
    spending_history: Dict[str, List[Decimal]] = field(default_factory=dict)

    def can_afford(self, cost: Decimal) -> bool:
        """Check if the agent can afford a given cost."""
        return self.budget >= cost

    def spend(self, amount: Decimal, agent_card_name: str) -> None:
        """Record a spending transaction and update budget tracking."""
        if not self.can_afford(amount):
            raise ValueError(
                f"Cannot afford {amount}. Current budget: {self.budget}")

        self.budget -= amount
        if agent_card_name not in self.spending_history:
            self.spending_history[agent_card_name] = []
        self.spending_history[agent_card_name].append(amount)
