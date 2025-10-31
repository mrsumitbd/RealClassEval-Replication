
from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from decimal import Decimal
from typing import List, Tuple


@dataclass
class BudgetTracker:
    """
    Tracks agent spending and budget decisions.
    Provides comprehensive budget management including affordability checks,
    spending tracking per agent card, and cost analysis over time.
    """

    # The total budget allocated to this agent card.
    budget: Decimal
    # The amount already spent from the budget.
    spent: Decimal = Decimal(0)
    # History of spending transactions: (amount, timestamp).
    history: List[Tuple[Decimal, datetime]] = field(default_factory=list)

    def can_afford(self, cost: Decimal) -> bool:
        """Check if the agent can afford a given cost."""
        return (self.budget - self.spent) >= cost

    def spend(self, amount: Decimal, agent_card_name: str) -> None:
        """
        Record a spending transaction and update budget tracking.

        Parameters
        ----------
        amount : Decimal
            The amount to spend.
        agent_card_name : str
            Identifier for the agent card (used only for logging purposes).

        Raises
        ------
        ValueError
            If the amount exceeds the remaining budget.
        """
        if not self.can_afford(amount):
            raise ValueError(
                f"Agent card '{agent_card_name}' cannot afford {amount}. "
                f"Remaining budget: {self.budget - self.spent}"
            )
        self.spent += amount
        self.history.append((amount, datetime.now()))
