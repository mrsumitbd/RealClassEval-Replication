from dataclasses import dataclass

@dataclass
class CostInfo:
    """A structured way to hold cost, token, and provider information."""
    provider: str
    input_tokens: int = 0
    output_tokens: int = 0
    input_cost_dollars: float = 0.0
    output_cost_dollars: float = 0.0

    @property
    def total_cost_dollars(self) -> float:
        return self.input_cost_dollars + self.output_cost_dollars

    def __add__(self, other: 'CostInfo') -> 'CostInfo':
        """Allows adding two CostInfo objects for easy aggregation."""
        return CostInfo(provider='', input_tokens=self.input_tokens + other.input_tokens, output_tokens=self.output_tokens + other.output_tokens, input_cost_dollars=self.input_cost_dollars + other.input_cost_dollars, output_cost_dollars=self.output_cost_dollars + other.output_cost_dollars)