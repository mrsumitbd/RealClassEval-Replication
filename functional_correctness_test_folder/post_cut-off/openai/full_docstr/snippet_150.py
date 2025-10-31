
from __future__ import annotations

from dataclasses import dataclass, field
from decimal import Decimal
from typing import Dict


@dataclass
class BudgetTracker:
    """
    Tracks agent spending and budget decisions.
    Provides comprehensive budget management including affordability checks,
    spending tracking per agent card, and cost analysis over time.
    """

    total_budget: Decimal
    spent: Dict[str, Decimal] = field(default_factory=dict)

    def can_afford(self, cost: Decimal) -> bool:
        """Check if the agent can afford a given cost."""
        used = sum(self.spent.values())
        return (self.total_budget - used) >= cost

    def spend(self, amount: Decimal, agent_card_name: str) -> None:
        """Record a spending transaction and update budget tracking."""
        if not self.can_afford(amount):
            raise ValueError("Insufficient budget to cover the amount.")
        self.spent[agent_card_name] = self.spent.get(
            agent_card_name, Decimal(0)) + amount
