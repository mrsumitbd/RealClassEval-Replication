
from typing import Optional, Dict, Any
from dataclasses import dataclass


@dataclass
class TokenCounts:
    input_tokens: int = 0
    output_tokens: int = 0
    cache_creation_tokens: int = 0
    cache_read_tokens: int = 0


class CostMode:
    pass  # Assuming this is an enum or similar; implementation not provided


class PricingCalculator:
    """Calculates costs based on model pricing with caching support.

    This class provides methods for calculating costs for individual models/tokens
    as well as detailed cost breakdowns for collections of usage entries.
    It supports custom pricing configurations and caches calculations for performance.
    Features:
    - Configurable pricing (from config or custom)
    - Fallback hardcoded pricing for robustness
    - Caching for performance
    - Support for all token types including cache
    - Backward compatible with both APIs
    """

    # Hardcoded default pricing
    MODEL_PRICING = {
        "gpt-4": {
            "input": 0.03 / 1000,
            "output": 0.06 / 1000,
            "cache_creation": 0.01 / 1000,
            "cache_read": 0.001 / 1000,
        },
        "gpt-3.5-turbo": {
            "input": 0.0015 / 1000,
            "output": 0.002 / 1000,
            "cache_creation": 0.0005 / 1000,
            "cache_read": 0.0001 / 1000,
        }
    }

    def __init__(self, custom_pricing: Optional[Dict[str, Dict[str, float]]] = None) -> None:
        """Initialize with optional custom pricing.

        Args:
            custom_pricing: Optional custom pricing dictionary to override defaults.
                          Should follow same structure as MODEL_PRICING.
        """
        self._pricing = self.MODEL_PRICING.copy()
        if custom_pricing:
            self._pricing.update(custom_pricing)
        self._cache: Dict[str, Dict[str, float]] = {}

    def calculate_cost(self, model: str, input_tokens: int = 0, output_tokens: int = 0,
                       cache_creation_tokens: int = 0, cache_read_tokens: int = 0,
                       tokens: Optional[TokenCounts] = None, strict: bool = False) -> float:
        """Calculate cost with flexible API supporting both signatures.

        Args:
            model: Model name
            input_tokens: Number of input tokens (ignored if tokens provided)
            output_tokens: Number of output tokens (ignored if tokens provided)
            cache_creation_tokens: Number of cache creation tokens
            cache_read_tokens: Number of cache read tokens
            tokens: Optional TokenCounts object (takes precedence)

        Returns:
            Total cost in USD
        """
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
        """Get pricing for a model with optional fallback logic.

        Args:
            model: Model name
            strict: If True, raise KeyError for unknown models

        Returns:
            Pricing dictionary with input/output/cache costs

        Raises:
            KeyError: If strict=True and model is unknown
        """
        if model in self._cache:
            return self._cache[model]

        if model in self._pricing:
            pricing = self._pricing[model]
            self._cache[model] = pricing
            return pricing

        if strict:
            raise KeyError(f"Unknown model: {model}")

        # Fallback to default pricing if available
        fallback_model = next(
            (m for m in self._pricing if model.startswith(m)), None)
        if fallback_model:
            pricing = self._pricing[fallback_model]
            self._cache[model] = pricing
            return pricing

        # Final fallback to GPT-3.5 pricing
        pricing = self._pricing["gpt-3.5-turbo"]
        self._cache[model] = pricing
        return pricing

    def calculate_cost_for_entry(self, entry_data: Dict[str, Any], mode: CostMode) -> float:
        """Calculate cost for a single entry (backward compatibility).

        Args:
            entry_data: Entry data dictionary
            mode: Cost mode (for backward compatibility)

        Returns:
            Cost in USD
        """
        model = entry_data.get("model", "gpt-3.5-turbo")
        tokens = entry_data.get("tokens", {})

        input_tokens = tokens.get("input", 0)
        output_tokens = tokens.get("output", 0)
        cache_creation_tokens = tokens.get("cache_creation", 0)
        cache_read_tokens = tokens.get("cache_read", 0)

        return self.calculate_cost(
            model=model,
            input_tokens=input_tokens,
            output_tokens=output_tokens,
            cache_creation_tokens=cache_creation_tokens,
            cache_read_tokens=cache_read_tokens
        )
