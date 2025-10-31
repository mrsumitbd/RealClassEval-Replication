
from typing import Dict, Optional, Any
from enum import Enum


class CostMode(Enum):
    INPUT = 1
    OUTPUT = 2
    CACHE_CREATION = 3
    CACHE_READ = 4


class TokenCounts:
    def __init__(self, input_tokens: int = 0, output_tokens: int = 0, cache_creation_tokens: int = 0, cache_read_tokens: int = 0):
        self.input_tokens = input_tokens
        self.output_tokens = output_tokens
        self.cache_creation_tokens = cache_creation_tokens
        self.cache_read_tokens = cache_read_tokens


class PricingCalculator:
    MODEL_PRICING = {
        'model1': {
            'input': 0.01,
            'output': 0.02,
            'cache_creation': 0.005,
            'cache_read': 0.001
        },
        'model2': {
            'input': 0.015,
            'output': 0.025,
            'cache_creation': 0.006,
            'cache_read': 0.002
        }
    }

    def __init__(self, custom_pricing: Optional[Dict[str, Dict[str, float]]] = None) -> None:
        self.pricing = self.MODEL_PRICING.copy()
        if custom_pricing:
            self.pricing.update(custom_pricing)

    def calculate_cost(self, model: str, input_tokens: int = 0, output_tokens: int = 0, cache_creation_tokens: int = 0, cache_read_tokens: int = 0, tokens: Optional[TokenCounts] = None, strict: bool = False) -> float:
        pricing = self._get_pricing_for_model(model, strict)
        if tokens:
            input_tokens = tokens.input_tokens
            output_tokens = tokens.output_tokens
            cache_creation_tokens = tokens.cache_creation_tokens
            cache_read_tokens = tokens.cache_read_tokens

        total_cost = (
            input_tokens * pricing['input'] +
            output_tokens * pricing['output'] +
            cache_creation_tokens * pricing['cache_creation'] +
            cache_read_tokens * pricing['cache_read']
        )
        return total_cost

    def _get_pricing_for_model(self, model: str, strict: bool = False) -> Dict[str, float]:
        if model in self.pricing:
            return self.pricing[model]
        if not strict:
            return self.pricing['default'] if 'default' in self.pricing else self.pricing[next(iter(self.pricing))]
        raise KeyError(f"Model '{model}' not found in pricing data")

    def calculate_cost_for_entry(self, entry_data: Dict[str, Any], mode: CostMode) -> float:
        model = entry_data.get('model', 'default')
        pricing = self._get_pricing_for_model(model)

        if mode == CostMode.INPUT:
            return entry_data.get('input_tokens', 0) * pricing['input']
        elif mode == CostMode.OUTPUT:
            return entry_data.get('output_tokens', 0) * pricing['output']
        elif mode == CostMode.CACHE_CREATION:
            return entry_data.get('cache_creation_tokens', 0) * pricing['cache_creation']
        elif mode == CostMode.CACHE_READ:
            return entry_data.get('cache_read_tokens', 0) * pricing['cache_read']
        else:
            raise ValueError(f"Unknown cost mode: {mode}")
