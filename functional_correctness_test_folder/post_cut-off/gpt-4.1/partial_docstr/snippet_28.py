
from typing import Optional, Dict, Any
from copy import deepcopy
from enum import Enum

# Dummy TokenCounts and CostMode for completeness


class TokenCounts:
    def __init__(self, input_tokens=0, output_tokens=0, cache_creation_tokens=0, cache_read_tokens=0):
        self.input_tokens = input_tokens
        self.output_tokens = output_tokens
        self.cache_creation_tokens = cache_creation_tokens
        self.cache_read_tokens = cache_read_tokens


class CostMode(Enum):
    DEFAULT = 0


MODEL_PRICING = {
    "gpt-3.5-turbo": {
        "input": 0.0015 / 1000,
        "output": 0.002 / 1000,
        "cache_creation": 0.0,
        "cache_read": 0.0,
    },
    "gpt-4": {
        "input": 0.03 / 1000,
        "output": 0.06 / 1000,
        "cache_creation": 0.0,
        "cache_read": 0.0,
    },
    "gpt-4-32k": {
        "input": 0.06 / 1000,
        "output": 0.12 / 1000,
        "cache_creation": 0.0,
        "cache_read": 0.0,
    },
    # Add more models as needed
}


class PricingCalculator:

    def __init__(self, custom_pricing: Optional[Dict[str, Dict[str, float]]] = None) -> None:
        if custom_pricing is not None:
            self.pricing = deepcopy(MODEL_PRICING)
            for model, prices in custom_pricing.items():
                if model not in self.pricing:
                    self.pricing[model] = {}
                self.pricing[model].update(prices)
        else:
            self.pricing = deepcopy(MODEL_PRICING)

    def calculate_cost(
        self,
        model: str,
        input_tokens: int = 0,
        output_tokens: int = 0,
        cache_creation_tokens: int = 0,
        cache_read_tokens: int = 0,
        tokens: Optional[TokenCounts] = None,
        strict: bool = False
    ) -> float:
        pricing = self._get_pricing_for_model(model, strict=strict)
        if tokens is not None:
            input_tokens = getattr(tokens, "input_tokens", 0)
            output_tokens = getattr(tokens, "output_tokens", 0)
            cache_creation_tokens = getattr(tokens, "cache_creation_tokens", 0)
            cache_read_tokens = getattr(tokens, "cache_read_tokens", 0)
        cost = (
            input_tokens * pricing.get("input", 0.0) +
            output_tokens * pricing.get("output", 0.0) +
            cache_creation_tokens * pricing.get("cache_creation", 0.0) +
            cache_read_tokens * pricing.get("cache_read", 0.0)
        )
        return cost

    def _get_pricing_for_model(self, model: str, strict: bool = False) -> Dict[str, float]:
        if model in self.pricing:
            return self.pricing[model]
        if strict:
            raise KeyError(f"Unknown model: {model}")
        # fallback: try to find a model with a prefix match (e.g., "gpt-4-32k-0613" -> "gpt-4-32k")
        for known_model in self.pricing:
            if model.startswith(known_model):
                return self.pricing[known_model]
        # fallback: try to find a model with a substring match
        for known_model in self.pricing:
            if known_model in model:
                return self.pricing[known_model]
        # fallback: use the first model as default
        return next(iter(self.pricing.values()))

    def calculate_cost_for_entry(self, entry_data: Dict[str, Any], mode: CostMode) -> float:
        model = entry_data.get("model", "")
        input_tokens = entry_data.get("input_tokens", 0)
        output_tokens = entry_data.get("output_tokens", 0)
        cache_creation_tokens = entry_data.get("cache_creation_tokens", 0)
        cache_read_tokens = entry_data.get("cache_read_tokens", 0)
        tokens = entry_data.get("tokens", None)
        return self.calculate_cost(
            model=model,
            input_tokens=input_tokens,
            output_tokens=output_tokens,
            cache_creation_tokens=cache_creation_tokens,
            cache_read_tokens=cache_read_tokens,
            tokens=tokens,
            strict=False
        )
