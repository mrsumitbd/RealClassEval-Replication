import threading
from typing import Optional, Dict, Any
from .types import TokenCounts, CostMode

# Example hardcoded pricing table (should be replaced with actual values)
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
        self._cost_cache = {}
        self._lock = threading.Lock()

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
        # Use tokens object if provided
        if tokens is not None:
            input_tokens = getattr(tokens, "input", 0)
            output_tokens = getattr(tokens, "output", 0)
            cache_creation_tokens = getattr(tokens, "cache_creation", 0)
            cache_read_tokens = getattr(tokens, "cache_read", 0)

        cache_key = (
            model, input_tokens, output_tokens, cache_creation_tokens, cache_read_tokens, strict
        )
        with self._lock:
            if cache_key in self._cost_cache:
                return self._cost_cache[cache_key]

        pricing = self._get_pricing_for_model(model, strict=strict)
        cost = (
            input_tokens * pricing.get("input", 0.0) +
            output_tokens * pricing.get("output", 0.0) +
            cache_creation_tokens * pricing.get("cache_creation", 0.0) +
            cache_read_tokens * pricing.get("cache_read", 0.0)
        )
        with self._lock:
            self._cost_cache[cache_key] = cost
        return cost

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
        with self._lock:
            if model in self._pricing_cache:
                return self._pricing_cache[model]

        # Check custom pricing first
        if model in self._custom_pricing:
            pricing = self._custom_pricing[model]
        elif model in MODEL_PRICING:
            pricing = MODEL_PRICING[model]
        else:
            if strict:
                raise KeyError(f"Unknown model for pricing: {model}")
            # Fallback: use the first available pricing as a default
            if self._custom_pricing:
                pricing = next(iter(self._custom_pricing.values()))
            else:
                pricing = next(iter(MODEL_PRICING.values()))
        with self._lock:
            self._pricing_cache[model] = pricing
        return pricing

    def calculate_cost_for_entry(self, entry_data: Dict[str, Any], mode: CostMode) -> float:
        '''Calculate cost for a single entry (backward compatibility).
        Args:
            entry_data: Entry data dictionary
            mode: Cost mode (for backward compatibility)
        Returns:
            Cost in USD
        '''
        # Try to extract tokens from entry_data
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
                input=input_tokens,
                output=output_tokens,
                cache_creation=cache_creation_tokens,
                cache_read=cache_read_tokens,
            )
        return self.calculate_cost(
            model,
            tokens=tokens,
            strict=False
        )
