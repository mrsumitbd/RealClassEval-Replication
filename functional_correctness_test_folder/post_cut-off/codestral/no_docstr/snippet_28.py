
from typing import Dict, Optional, Any
from enum import Enum


class CostMode(Enum):
    INPUT = "input"
    OUTPUT = "output"
    CACHE_CREATION = "cache_creation"
    CACHE_READ = "cache_read"


class TokenCounts:
    def __init__(self, input_tokens: int = 0, output_tokens: int = 0, cache_creation_tokens: int = 0, cache_read_tokens: int = 0) -> None:
        self.input_tokens = input_tokens
        self.output_tokens = output_tokens
        self.cache_creation_tokens = cache_creation_tokens
        self.cache_read_tokens = cache_read_tokens


class PricingCalculator:
    DEFAULT_PRICING = {
        "gpt-3.5-turbo": {
            "input": 0.0015,
            "output": 0.002,
            "cache_creation": 0.0015,
            "cache_read": 0.0005
        },
        "gpt-4": {
            "input": 0.03,
            "output": 0.06,
            "cache_creation": 0.03,
            "cache_read": 0.01
        }
    }

    def __init__(self, custom_pricing: Optional[Dict[str, Dict[str, float]]] = None) -> None:
        self.pricing = self.DEFAULT_PRICING.copy()
        if custom_pricing:
            self.pricing.update(custom_pricing)

    def calculate_cost(self, model: str, input_tokens: int = 0, output_tokens: int = 0, cache_creation_tokens: int = 0, cache_read_tokens: int = 0, tokens: Optional[TokenCounts] = None, strict: bool = False) -> float:
        if tokens:
            input_tokens = tokens.input_tokens
            output_tokens = tokens.output_tokens
            cache_creation_tokens = tokens.cache_creation_tokens
            cache_read_tokens = tokens.cache_read_tokens

        pricing = self._get_pricing_for_model(model, strict)
        cost = (
            input_tokens * pricing["input"] +
            output_tokens * pricing["output"] +
            cache_creation_tokens * pricing["cache_creation"] +
            cache_read_tokens * pricing["cache_read"]
        )
        return cost

    def _get_pricing_for_model(self, model: str, strict: bool = False) -> Dict[str, float]:
        if model not in self.pricing:
            if strict:
                raise ValueError(f"Model {model} not found in pricing data")
            else:
                return self.pricing["gpt-3.5-turbo"]
        return self.pricing[model]

    def calculate_cost_for_entry(self, entry_data: Dict[str, Any], mode: CostMode) -> float:
        model = entry_data.get("model", "gpt-3.5-turbo")
        pricing = self._get_pricing_for_model(model)

        if mode == CostMode.INPUT:
            tokens = entry_data.get("input_tokens", 0)
        elif mode == CostMode.OUTPUT:
            tokens = entry_data.get("output_tokens", 0)
        elif mode == CostMode.CACHE_CREATION:
            tokens = entry_data.get("cache_creation_tokens", 0)
        elif mode == CostMode.CACHE_READ:
            tokens = entry_data.get("cache_read_tokens", 0)
        else:
            raise ValueError(f"Invalid cost mode: {mode}")

        return tokens * pricing[mode.value]
