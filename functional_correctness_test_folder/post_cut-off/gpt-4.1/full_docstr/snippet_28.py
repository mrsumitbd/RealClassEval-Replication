
from typing import Optional, Dict, Any
from functools import lru_cache

# Dummy types for compatibility


class TokenCounts:
    def __init__(self, input_tokens=0, output_tokens=0, cache_creation_tokens=0, cache_read_tokens=0):
        self.input_tokens = input_tokens
        self.output_tokens = output_tokens
        self.cache_creation_tokens = cache_creation_tokens
        self.cache_read_tokens = cache_read_tokens


class CostMode:
    # Placeholder for backward compatibility
    pass


# Hardcoded fallback pricing
MODEL_PRICING = {
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
    },
    "gpt-4-turbo": {
        "input": 0.01 / 1000,
        "output": 0.03 / 1000,
        "cache_creation": 0.003 / 1000,
        "cache_read": 0.001 / 1000,
    },
    # Add more models as needed
}


class PricingCalculator:
    '''Calculates costs based on model pricing with caching support.
    This class provides methods for calculating costs for individual models/tokens
    as well as detailed cost breakdowns for collections of usage entries.
    It supports custom pricing configurations and caches calculations for performance.
    Features:
    - Configurable pricing (from config or custom)
    - Fallback hardcoded pricing for robustness
    - Caching for performance
    - Support for all token types including cache
    - Backward compatible with both APIs
    '''

    def __init__(self, custom_pricing: Optional[Dict[str, Dict[str, float]]] = None) -> None:
        '''Initialize with optional custom pricing.
        Args:
            custom_pricing: Optional custom pricing dictionary to override defaults.
                          Should follow same structure as MODEL_PRICING.
        '''
        self._custom_pricing = custom_pricing or {}
        self._pricing_cache = {}

    @lru_cache(maxsize=128)
    def _get_pricing_for_model(self, model: str, strict: bool = False) -> Dict[str, float]:
        '''Get pricing for a model with optional fallback logic.
        Args:
            model: Model name
            strict: If True, raise KeyError for unknown models
        Returns:
            Pricing dictionary with input/output/cache costs
        Raises:
            KeyError: If strict=True and model is unknown
        '''
        # Check custom pricing first
        if model in self._custom_pricing:
            return self._custom_pricing[model]
        # Fallback to hardcoded pricing
        if model in MODEL_PRICING:
            return MODEL_PRICING[model]
        # Try to match by prefix (e.g., "gpt-3.5-turbo-0613" -> "gpt-3.5-turbo")
        for known in list(self._custom_pricing.keys()) + list(MODEL_PRICING.keys()):
            if model.startswith(known):
                if known in self._custom_pricing:
                    return self._custom_pricing[known]
                else:
                    return MODEL_PRICING[known]
        if strict:
            raise KeyError(f"Unknown model for pricing: {model}")
        # Fallback to gpt-3.5-turbo as a last resort
        return MODEL_PRICING["gpt-3.5-turbo"]

    def calculate_cost(self, model: str, input_tokens: int = 0, output_tokens: int = 0, cache_creation_tokens: int = 0, cache_read_tokens: int = 0, tokens: Optional[TokenCounts] = None, strict: bool = False) -> float:
        '''Calculate cost with flexible API supporting both signatures.
        Args:
            model: Model name
            input_tokens: Number of input tokens (ignored if tokens provided)
            output_tokens: Number of output tokens (ignored if tokens provided)
            cache_creation_tokens: Number of cache creation tokens
            cache_read_tokens: Number of cache read tokens
            tokens: Optional TokenCounts object (takes precedence)
        Returns:
            Total cost in USD
        '''
        if tokens is not None:
            input_tokens = getattr(tokens, "input_tokens", 0)
            output_tokens = getattr(tokens, "output_tokens", 0)
            cache_creation_tokens = getattr(tokens, "cache_creation_tokens", 0)
            cache_read_tokens = getattr(tokens, "cache_read_tokens", 0)
        # Use a cache for performance
        cache_key = (
            model, input_tokens, output_tokens, cache_creation_tokens, cache_read_tokens, strict
        )
        if cache_key in self._pricing_cache:
            return self._pricing_cache[cache_key]
        pricing = self._get_pricing_for_model(model, strict)
        cost = (
            input_tokens * pricing.get("input", 0.0) +
            output_tokens * pricing.get("output", 0.0) +
            cache_creation_tokens * pricing.get("cache_creation", 0.0) +
            cache_read_tokens * pricing.get("cache_read", 0.0)
        )
        self._pricing_cache[cache_key] = cost
        return cost

    def calculate_cost_for_entry(self, entry_data: Dict[str, Any], mode: CostMode) -> float:
        '''Calculate cost for a single entry (backward compatibility).
        Args:
            entry_data: Entry data dictionary
            mode: Cost mode (for backward compatibility)
        Returns:
            Cost in USD
        '''
        # Try to extract tokens in both old and new formats
        model = entry_data.get("model") or entry_data.get("model_name")
        tokens = None
        if "tokens" in entry_data and isinstance(entry_data["tokens"], TokenCounts):
            tokens = entry_data["tokens"]
        else:
            input_tokens = entry_data.get("input_tokens", 0)
            output_tokens = entry_data.get("output_tokens", 0)
            cache_creation_tokens = entry_data.get("cache_creation_tokens", 0)
            cache_read_tokens = entry_data.get("cache_read_tokens", 0)
            tokens = TokenCounts(
                input_tokens=input_tokens,
                output_tokens=output_tokens,
                cache_creation_tokens=cache_creation_tokens,
                cache_read_tokens=cache_read_tokens,
            )
        return self.calculate_cost(model, tokens=tokens)
