
from dataclasses import dataclass
from decimal import Decimal


@dataclass
class BudgetTracker:
    balance: Decimal = Decimal('0.00')

    def can_afford(self, cost: Decimal) -> bool:
        return self.balance >= cost

    def spend(self, amount: Decimal, agent_card_name: str) -> None:
        if self.can_afford(amount):
            self.balance -= amount
        else:
            raise ValueError(f"Insufficient funds for {agent_card_name}")
