
from dataclasses import dataclass, field
from decimal import Decimal
from typing import Dict


@dataclass
class BudgetTracker:
    """Tracks expenses and checks if a certain cost can be afforded."""
    budget: Decimal = field(default=Decimal('0.0'))
    expenses: Dict[str, Decimal] = field(default_factory=dict)

    def can_afford(self, cost: Decimal) -> bool:
        """Checks if the tracker has enough budget to afford a certain cost."""
        return self.budget >= cost

    def spend(self, amount: Decimal, agent_card_name: str) -> None:
        """Spends a certain amount from the budget and records the expense."""
        if not self.can_afford(amount):
            raise ValueError("Insufficient budget")

        self.budget -= amount
        self.expenses[agent_card_name] = self.expenses.get(
            agent_card_name, Decimal('0.0')) + amount
