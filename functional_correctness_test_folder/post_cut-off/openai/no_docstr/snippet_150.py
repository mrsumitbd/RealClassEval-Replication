
from __future__ import annotations
from dataclasses import dataclass, field
from decimal import Decimal
from typing import Dict


@dataclass
class BudgetTracker:
    total_budget: Decimal
    spent: Decimal = field(default_factory=lambda: Decimal("0"))
    per_agent_spent: Dict[str, Decimal] = field(default_factory=dict)

    def can_afford(self, cost: Decimal) -> bool:
        """Return True if the remaining budget can cover the given cost."""
        if cost < 0:
            raise ValueError("Cost must be non‑negative")
        return cost <= (self.total_budget - self.spent)

    def spend(self, amount: Decimal, agent_card_name: str) -> None:
        """Record a spend of `amount` for the specified agent card."""
        if amount < 0:
            raise ValueError("Amount must be non‑negative")
        if not self.can_afford(amount):
            raise ValueError("Insufficient budget to cover the spend")

        # Update total spent
        self.spent += amount

        # Update per‑agent spent
        current = self.per_agent_spent.get(agent_card_name, Decimal("0"))
        self.per_agent_spent[agent_card_name] = current + amount
