from dataclasses import dataclass, field
from decimal import Decimal, ROUND_HALF_UP, InvalidOperation
from datetime import datetime
from typing import Dict, List


@dataclass(frozen=True)
class BudgetTransaction:
    timestamp: datetime
    agent_card_name: str
    amount: Decimal
    remaining_budget: Decimal
    total_spent: Decimal


@dataclass
class BudgetTracker:
    '''
    Tracks agent spending and budget decisions.
    Provides comprehensive budget management including affordability checks,
    spending tracking per agent card, and cost analysis over time.
    '''
    budget: Decimal
    allow_overdraft: bool = False
    overdraft_limit: Decimal = Decimal('0')
    quantize_to: Decimal = Decimal('0.01')

    spent: Decimal = field(default=Decimal('0'), init=False)
    spend_by_card: Dict[str, Decimal] = field(default_factory=dict, init=False)
    transactions: List[BudgetTransaction] = field(
        default_factory=list, init=False)

    def __post_init__(self) -> None:
        self.budget = self._coerce_decimal(self.budget)
        self.overdraft_limit = self._coerce_decimal(self.overdraft_limit)
        self.quantize_to = self._coerce_decimal(self.quantize_to)
        if self.quantize_to <= 0:
            raise ValueError(
                'quantize_to must be a positive Decimal (e.g., 0.01)')
        if self.budget < 0:
            raise ValueError('budget cannot be negative')
        if self.overdraft_limit < 0:
            raise ValueError('overdraft_limit cannot be negative')
        # Quantize initial values
        self.budget = self._q(self.budget)
        self.overdraft_limit = self._q(self.overdraft_limit)
        self.spent = self._q(Decimal('0'))

    def _coerce_decimal(self, value) -> Decimal:
        if isinstance(value, Decimal):
            return value
        try:
            return Decimal(str(value))
        except (InvalidOperation, ValueError, TypeError) as e:
            raise ValueError(f'invalid decimal value: {value}') from e

    def _q(self, value: Decimal) -> Decimal:
        return self._coerce_decimal(value).quantize(self.quantize_to, rounding=ROUND_HALF_UP)

    @property
    def available_funds(self) -> Decimal:
        limit = self.budget + \
            (self.overdraft_limit if self.allow_overdraft else Decimal('0'))
        return self._q(limit - self.spent)

    def can_afford(self, cost: Decimal) -> bool:
        '''Check if the agent can afford a given cost.'''
        amount = self._q(self._coerce_decimal(cost))
        if amount < 0:
            raise ValueError('cost cannot be negative')
        return amount <= self.available_funds

    def spend(self, amount: Decimal, agent_card_name: str) -> None:
        '''Record a spending transaction and update budget tracking.'''
        if not agent_card_name or not isinstance(agent_card_name, str):
            raise ValueError('agent_card_name must be a non-empty string')
        amt = self._q(self._coerce_decimal(amount))
        if amt <= 0:
            raise ValueError('amount must be greater than zero')
        if not self.can_afford(amt):
            raise ValueError('insufficient funds')

        self.spent = self._q(self.spent + amt)
        self.spend_by_card[agent_card_name] = self._q(
            self.spend_by_card.get(agent_card_name, Decimal('0')) + amt)
        remaining = self.available_funds
        self.transactions.append(
            BudgetTransaction(
                timestamp=datetime.utcnow(),
                agent_card_name=agent_card_name,
                amount=amt,
                remaining_budget=remaining,
                total_spent=self.spent,
            )
        )
