
from typing import Dict, Optional, Any
from dataclasses import dataclass


@dataclass
class TokenCounts:
    input_tokens: int = 0
    output_tokens: int = 0
    cache_creation_tokens: int = 0
    cache_read_tokens: int = 0


class CostMode:
    pass


MODEL_PRICING = {
    "gpt-3.5-turbo": {
        "input": 0.0015,
        "output": 0.002,
        "cache_creation": 0.0005,
        "cache_read": 0.0001
    },
    "gpt-4": {
        "input": 0.03,
        "output": 0.06,
        "cache_creation": 0.001,
        "cache_read": 0.0002
    }
}


class PricingCalculator:

    def __init__(self, custom_pricing: Optional[Dict[str, Dict[str, float]]] = None) -> None:
        self.pricing = MODEL_PRICING.copy()
        if custom_pricing:
            self.pricing.update(custom_pricing)

    def calculate_cost(self, model: str, input_tokens: int = 0, output_tokens: int = 0, cache_creation_tokens: int = 0, cache_read_tokens: int = 0, tokens: Optional[TokenCounts] = None, strict: bool = False) -> float:
        if tokens is not None:
            input_tokens = tokens.input_tokens
            output_tokens = tokens.output_tokens
            cache_creation_tokens = tokens.cache_creation_tokens
            cache_read_tokens = tokens.cache_read_tokens

        pricing = self._get_pricing_for_model(model, strict)

        input_cost = input_tokens * pricing.get("input", 0)
        output_cost = output_tokens * pricing.get("output", 0)
        cache_creation_cost = cache_creation_tokens * \
            pricing.get("cache_creation", 0)
        cache_read_cost = cache_read_tokens * pricing.get("cache_read", 0)

        return input_cost + output_cost + cache_creation_cost + cache_read_cost

    def _get_pricing_for_model(self, model: str, strict: bool = False) -> Dict[str, float]:
        if strict and model not in self.pricing:
            raise KeyError(f"Model {model} not found in pricing data")
        return self.pricing.get(model, {})

    def calculate_cost_for_entry(self, entry_data: Dict[str, Any], mode: CostMode) -> float:
        model = entry_data.get("model", "")
        input_tokens = entry_data.get("input_tokens", 0)
        output_tokens = entry_data.get("output_tokens", 0)
        cache_creation_tokens = entry_data.get("cache_creation_tokens", 0)
        cache_read_tokens = entry_data.get("cache_read_tokens", 0)

        return self.calculate_cost(
            model=model,
            input_tokens=input_tokens,
            output_tokens=output_tokens,
            cache_creation_tokens=cache_creation_tokens,
            cache_read_tokens=cache_read_tokens
        )
