
from typing import Dict, Optional, Any


class TokenCounts:
    pass


class CostMode:
    pass


class PricingCalculator:

    def __init__(self, custom_pricing: Optional[Dict[str, Dict[str, float]]] = None) -> None:
        self.default_pricing = {
            "gpt-3.5-turbo": {
                "input": 0.0015,
                "output": 0.002,
                "cache_creation": 0.0005,
                "cache_read": 0.0001
            },
            "gpt-4": {
                "input": 0.03,
                "output": 0.06,
                "cache_creation": 0.01,
                "cache_read": 0.001
            }
        }
        self.custom_pricing = custom_pricing if custom_pricing is not None else {}

    def calculate_cost(self, model: str, input_tokens: int = 0, output_tokens: int = 0, cache_creation_tokens: int = 0, cache_read_tokens: int = 0, tokens: Optional[TokenCounts] = None, strict: bool = False) -> float:
        pricing = self._get_pricing_for_model(model, strict)

        if tokens is not None:
            input_tokens = getattr(tokens, 'input_tokens', input_tokens)
            output_tokens = getattr(tokens, 'output_tokens', output_tokens)
            cache_creation_tokens = getattr(
                tokens, 'cache_creation_tokens', cache_creation_tokens)
            cache_read_tokens = getattr(
                tokens, 'cache_read_tokens', cache_read_tokens)

        input_cost = (input_tokens / 1000) * pricing.get('input', 0)
        output_cost = (output_tokens / 1000) * pricing.get('output', 0)
        cache_creation_cost = (cache_creation_tokens / 1000) * \
            pricing.get('cache_creation', 0)
        cache_read_cost = (cache_read_tokens / 1000) * \
            pricing.get('cache_read', 0)

        total_cost = input_cost + output_cost + cache_creation_cost + cache_read_cost
        return total_cost

    def _get_pricing_for_model(self, model: str, strict: bool = False) -> Dict[str, float]:
        if model in self.custom_pricing:
            return self.custom_pricing[model]
        if model in self.default_pricing:
            return self.default_pricing[model]
        if strict:
            raise ValueError(f"No pricing found for model: {model}")
        return {
            "input": 0.0,
            "output": 0.0,
            "cache_creation": 0.0,
            "cache_read": 0.0
        }

    def calculate_cost_for_entry(self, entry_data: Dict[str, Any], mode: CostMode) -> float:
        model = entry_data.get('model', '')
        input_tokens = entry_data.get('input_tokens', 0)
        output_tokens = entry_data.get('output_tokens', 0)
        cache_creation_tokens = entry_data.get('cache_creation_tokens', 0)
        cache_read_tokens = entry_data.get('cache_read_tokens', 0)

        return self.calculate_cost(
            model=model,
            input_tokens=input_tokens,
            output_tokens=output_tokens,
            cache_creation_tokens=cache_creation_tokens,
            cache_read_tokens=cache_read_tokens
        )
