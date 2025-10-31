
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

    # Mapping of agent card name to its allocated budget
    budgets: Dict[str, Decimal] = field(default_factory=dict)
    # Mapping of agent card name to the total amount spent so far
    spent: Dict[str, Decimal] = field(default_factory=dict)
    # History of all spending transactions: (timestamp, agent_card_name, amount)
    history: List[Tuple[datetime, str, Decimal]] = field(default_factory=list)

    def can_afford(self, cost: Decimal, agent_card_name: str) -> bool:
        """
        Check if the agent can afford a given cost.

        Parameters
        ----------
        cost : Decimal
            The amount to be spent.
        agent_card_name : str
            Identifier of the agent card.

        Returns
        -------
        bool
            True if the cost does not exceed the remaining budget for the
            specified agent card, False otherwise.
        """
        budget = self.budgets.get(agent_card_name, Decimal("0"))
        spent_so_far = self.spent.get(agent_card_name, Decimal("0"))
        remaining = budget - spent_so_far
        return cost <= remaining

    def spend(self, amount: Decimal, agent_card_name: str) -> None:
        """
        Record a spending transaction and update budget tracking.

        Parameters
        ----------
        amount : Decimal
            The amount to be spent.
        agent_card_name : str
            Identifier of the agent card.

        Raises
        ------
        ValueError
            If the agent does not have enough remaining budget to cover the
            requested amount.
        """
        if not self.can_afford(amount, agent_card_name):
            raise ValueError(
                f"Agent '{agent_card_name}' cannot afford {amount}. "
                f"Remaining budget: {self.budgets.get(agent_card_name, Decimal('0')) - self.spent.get(agent_card_name, Decimal('0'))}"
            )

        # Update spent amount
        self.spent[agent_card_name] = self.spent.get(
            agent_card_name, Decimal("0")) + amount
        # Record transaction in history
        self.history.append((datetime.utcnow(), agent_card_name, amount))
