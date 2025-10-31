
from typing import Optional, Dict, Any
from enum import Enum


class CostMode(Enum):
    STANDARD = 1
    CACHE_CREATION = 2
    CACHE_READ = 3


class TokenCounts:
    def __init__(self, input_tokens=0, output_tokens=0, cache_creation_tokens=0, cache_read_tokens=0):
        self.input_tokens = input_tokens
        self.output_tokens = output_tokens
        self.cache_creation_tokens = cache_creation_tokens
        self.cache_read_tokens = cache_read_tokens


class PricingCalculator:

    DEFAULT_PRICING = {
        "gpt-3.5-turbo": {
            "input": 0.0015 / 1000,
            "output": 0.002 / 1000,
            "cache_creation": 0.0005 / 1000,
            "cache_read": 0.0001 / 1000,
        },
        "gpt-4": {
            "input": 0.03 / 1000,
            "output": 0.06 / 1000,
            "cache_creation": 0.01 / 1000,
            "cache_read": 0.002 / 1000,
        }
    }

    def __init__(self, custom_pricing: Optional[Dict[str, Dict[str, float]]] = None) -> None:
        self.pricing = self.DEFAULT_PRICING.copy()
        if custom_pricing:
            for model, prices in custom_pricing.items():
                if model not in self.pricing:
                    self.pricing[model] = {}
                self.pricing[model].update(prices)

    def calculate_cost(self, model: str, input_tokens: int = 0, output_tokens: int = 0, cache_creation_tokens: int = 0, cache_read_tokens: int = 0, tokens: Optional[TokenCounts] = None, strict: bool = False) -> float:
        if tokens is not None:
            input_tokens = tokens.input_tokens
            output_tokens = tokens.output_tokens
            cache_creation_tokens = tokens.cache_creation_tokens
            cache_read_tokens = tokens.cache_read_tokens
        pricing = self._get_pricing_for_model(model, strict=strict)
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
        if not strict:
            # fallback to first model in pricing
            return next(iter(self.pricing.values()))
        raise ValueError(
            f"Pricing for model '{model}' not found and strict mode is enabled.")

    def calculate_cost_for_entry(self, entry_data: Dict[str, Any], mode: CostMode) -> float:
        model = entry_data.get("model")
        if "tokens" in entry_data and isinstance(entry_data["tokens"], TokenCounts):
            tokens = entry_data["tokens"]
        else:
            tokens = TokenCounts(
                input_tokens=entry_data.get("input_tokens", 0),
                output_tokens=entry_data.get("output_tokens", 0),
                cache_creation_tokens=entry_data.get(
                    "cache_creation_tokens", 0),
                cache_read_tokens=entry_data.get("cache_read_tokens", 0),
            )
        pricing = self._get_pricing_for_model(model)
        if mode == CostMode.STANDARD:
            cost = (
                tokens.input_tokens * pricing.get("input", 0.0) +
                tokens.output_tokens * pricing.get("output", 0.0)
            )
        elif mode == CostMode.CACHE_CREATION:
            cost = tokens.cache_creation_tokens * \
                pricing.get("cache_creation", 0.0)
        elif mode == CostMode.CACHE_READ:
            cost = tokens.cache_read_tokens * pricing.get("cache_read", 0.0)
        else:
            cost = 0.0
        return cost
