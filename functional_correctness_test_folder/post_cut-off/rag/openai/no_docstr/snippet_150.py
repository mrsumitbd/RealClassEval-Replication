
from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from decimal import Decimal
from typing import Dict, List, Tuple


@dataclass
class BudgetTracker:
    """
    Tracks agent spending and budget decisions.
    Provides comprehensive budget management including affordability checks,
    spending tracking per agent card, and cost analysis over time.
    """

    # The total budget available for all agents.
    total_budget: Decimal

    # Total amount spent so far.
    spent: Decimal = field(default_factory=lambda: Decimal("0"))

    # Mapping from agent card name to the amount spent by that card.
    per_agent_card: Dict[str, Decimal] = field(default_factory=dict)

    # History of spending transactions: (timestamp, amount, agent_card_name).
    history: List[Tuple[datetime, Decimal, str]] = field(default_factory=list)

    def can_afford(self, cost: Decimal) -> bool:
        """Check if the agent can afford a given cost."""
        remaining = self.total_budget - self.spent
        return cost <= remaining

    def spend(self, amount: Decimal, agent_card_name: str) -> None:
        """Record a spending transaction and update budget tracking."""
        if not self.can_afford(amount):
            raise ValueError(
                f"Cannot afford amount {amount}. "
                f"Remaining budget: {self.total_budget - self.spent}"
            )
        # Update total spent
        self.spent += amount

        # Update per-agent card spending
        self.per_agent_card[agent_card_name] = self.per_agent_card.get(
            agent_card_name, Decimal("0")
        ) + amount

        # Record transaction in history
        self.history.append((datetime.utcnow(), amount, agent_card_name))
