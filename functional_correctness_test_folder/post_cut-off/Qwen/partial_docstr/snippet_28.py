
from typing import Optional, Dict, Any
from enum import Enum


class CostMode(Enum):
    INPUT = 'input'
    OUTPUT = 'output'
    CACHE_CREATION = 'cache_creation'
    CACHE_READ = 'cache_read'


class TokenCounts:
    def __init__(self, input_tokens: int, output_tokens: int, cache_creation_tokens: int, cache_read_tokens: int):
        self.input_tokens = input_tokens
        self.output_tokens = output_tokens
        self.cache_creation_tokens = cache_creation_tokens
        self.cache_read_tokens = cache_read_tokens


MODEL_PRICING = {
    'model1': {'input': 0.001, 'output': 0.002, 'cache_creation': 0.003, 'cache_read': 0.004},
    'model2': {'input': 0.002, 'output': 0.003, 'cache_creation': 0.004, 'cache_read': 0.005},
    # Add more models as needed
}


class PricingCalculator:

    def __init__(self, custom_pricing: Optional[Dict[str, Dict[str, float]]] = None) -> None:
        self.pricing = custom_pricing if custom_pricing is not None else MODEL_PRICING

    def calculate_cost(self, model: str, input_tokens: int = 0, output_tokens: int = 0, cache_creation_tokens: int = 0, cache_read_tokens: int = 0, tokens: Optional[TokenCounts] = None, strict: bool = False) -> float:
        if tokens is not None:
            input_tokens = tokens.input_tokens
            output_tokens = tokens.output_tokens
            cache_creation_tokens = tokens.cache_creation_tokens
            cache_read_tokens = tokens.cache_read_tokens

        pricing = self._get_pricing_for_model(model, strict)
        return (input_tokens * pricing['input'] +
                output_tokens * pricing['output'] +
                cache_creation_tokens * pricing['cache_creation'] +
                cache_read_tokens * pricing['cache_read'])

    def _get_pricing_for_model(self, model: str, strict: bool = False) -> Dict[str, float]:
        if model not in self.pricing:
            if strict:
                raise KeyError(f"Model {model} not found in pricing.")
            return {'input': 0.0, 'output': 0.0, 'cache_creation': 0.0, 'cache_read': 0.0}
        return self.pricing[model]

    def calculate_cost_for_entry(self, entry_data: Dict[str, Any], mode: CostMode) -> float:
        model = entry_data.get('model', '')
        if mode == CostMode.INPUT:
            tokens = entry_data.get('input_tokens', 0)
        elif mode == CostMode.OUTPUT:
            tokens = entry_data.get('output_tokens', 0)
        elif mode == CostMode.CACHE_CREATION:
            tokens = entry_data.get('cache_creation_tokens', 0)
        elif mode == CostMode.CACHE_READ:
            tokens = entry_data.get('cache_read_tokens', 0)
        else:
            raise ValueError(f"Unknown cost mode: {mode}")

        return self.calculate_cost(model, **{f"{mode.value}_tokens": tokens})
