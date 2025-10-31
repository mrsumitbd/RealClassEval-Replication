
from __future__ import annotations

from dataclasses import dataclass, field
from decimal import Decimal
from datetime import datetime
from typing import Dict, List, Tuple


@dataclass
class BudgetTracker:
    """
    Tracks agent spending and budget decisions.
    Provides comprehensive budget management including affordability checks,
    spending tracking per agent card, and cost analysis over time.
    """

    total_budget: Decimal
    spent: Dict[str, Decimal] = field(default_factory=dict)
    history: List[Tuple[datetime, Decimal, str]] = field(default_factory=list)

    def __post_init__(self) -> None:
        if not isinstance(self.total_budget, Decimal):
            raise TypeError("total_budget must be a Decimal")
        if self.total_budget < Decimal("0"):
            raise ValueError("total_budget cannot be negative")

    @property
    def remaining_budget(self) -> Decimal:
        """Return the remaining budget."""
        spent_total = sum(self.spent.values(), Decimal("0"))
        return self.total_budget - spent_total

    def can_afford(self, cost: Decimal) -> bool:
        """
        Check if the given cost can be afforded with the remaining budget.

        Parameters
        ----------
        cost : Decimal
            The cost to check.

        Returns
        -------
        bool
            True if the cost is less than or equal to the remaining budget,
            False otherwise.
        """
        if not isinstance(cost, Decimal):
            raise TypeError("cost must be a Decimal")
        if cost < Decimal("0"):
            raise ValueError("cost cannot be negative")
        return cost <= self.remaining_budget

    def spend(self, amount: Decimal, agent_card_name: str) -> None:
        """
        Record a spending transaction for a specific agent card.

        Parameters
        ----------
        amount : Decimal
            The amount to spend.
        agent_card_name : str
            The name of the agent card.

        Raises
        ------
        ValueError
            If the amount is negative or if the transaction would exceed the
            remaining budget.
        """
        if not isinstance(amount, Decimal):
            raise TypeError("amount must be a Decimal")
        if not isinstance(agent_card_name, str):
            raise TypeError("agent_card_name must be a string")
        if amount < Decimal("0"):
            raise ValueError("amount cannot be negative")

        if not self.can_afford(amount):
            raise ValueError(
                f"Cannot afford {amount}. Remaining budget: {self.remaining_budget}"
            )

        # Update spent per card
        self.spent[agent_card_name] = self.spent.get(
            agent_card_name, Decimal("0")) + amount

        # Record the transaction in history
        self.history.append((datetime.utcnow(), amount, agent_card_name))

    # Optional helper methods for analysis

    def total_spent(self) -> Decimal:
        """Return the total amount spent across all cards."""
        return sum(self.spent.values(), Decimal("0"))

    def spent_by_card(self, card_name: str) -> Decimal:
        """Return the amount spent by a specific card."""
        return self.spent.get(card_name, Decimal("0"))

    def spending_history(self) -> List[Tuple[datetime, Decimal, str]]:
        """Return a copy of the spending history."""
        return list(self.history)
