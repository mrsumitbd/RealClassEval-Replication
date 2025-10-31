
from typing import Optional, Dict, Any
from enum import Enum


class CostMode(Enum):
    DEFAULT = 1
    CUSTOM = 2


class TokenCounts:
    def __init__(self, input_tokens: int, output_tokens: int, cache_creation_tokens: int, cache_read_tokens: int):
        self.input_tokens = input_tokens
        self.output_tokens = output_tokens
        self.cache_creation_tokens = cache_creation_tokens
        self.cache_read_tokens = cache_read_tokens


class PricingCalculator:

    def __init__(self, custom_pricing: Optional[Dict[str, Dict[str, float]]] = None) -> None:
        self.default_pricing = {
            'model1': {'input': 0.001, 'output': 0.002, 'cache_creation': 0.0015, 'cache_read': 0.0005},
            'model2': {'input': 0.002, 'output': 0.003, 'cache_creation': 0.002, 'cache_read': 0.001}
        }
        self.custom_pricing = custom_pricing if custom_pricing is not None else {}

    def calculate_cost(self, model: str, input_tokens: int = 0, output_tokens: int = 0, cache_creation_tokens: int = 0, cache_read_tokens: int = 0, tokens: Optional[TokenCounts] = None, strict: bool = False) -> float:
        if tokens:
            input_tokens = tokens.input_tokens
            output_tokens = tokens.output_tokens
            cache_creation_tokens = tokens.cache_creation_tokens
            cache_read_tokens = tokens.cache_read_tokens

        pricing = self._get_pricing_for_model(model, strict)
        cost = (input_tokens * pricing['input'] +
                output_tokens * pricing['output'] +
                cache_creation_tokens * pricing['cache_creation'] +
                cache_read_tokens * pricing['cache_read'])
        return cost

    def _get_pricing_for_model(self, model: str, strict: bool = False) -> Dict[str, float]:
        if model in self.custom_pricing:
            return self.custom_pricing[model]
        elif not strict:
            return self.default_pricing.get(model, self.default_pricing['model1'])
        else:
            raise ValueError(f"No pricing found for model: {model}")

    def calculate_cost_for_entry(self, entry_data: Dict[str, Any], mode: CostMode) -> float:
        model = entry_data.get('model')
        input_tokens = entry_data.get('input_tokens', 0)
        output_tokens = entry_data.get('output_tokens', 0)
        cache_creation_tokens = entry_data.get('cache_creation_tokens', 0)
        cache_read_tokens = entry_data.get('cache_read_tokens', 0)

        if mode == CostMode.CUSTOM:
            return self.calculate_cost(model, input_tokens, output_tokens, cache_creation_tokens, cache_read_tokens, strict=True)
        else:
            return self.calculate_cost(model, input_tokens, output_tokens, cache_creation_tokens, cache_read_tokens)
