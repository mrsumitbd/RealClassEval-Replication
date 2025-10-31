import threading
from typing import Optional, Dict, Any
from collections.abc import Mapping
from functools import lru_cache

# Dummy types for illustration; replace with actual imports in your codebase
try:
    from .types import TokenCounts, CostMode
except ImportError:
    class TokenCounts:
        def __init__(self, input_tokens=0, output_tokens=0, cache_creation_tokens=0, cache_read_tokens=0):
            self.input_tokens = input_tokens
            self.output_tokens = output_tokens
            self.cache_creation_tokens = cache_creation_tokens
            self.cache_read_tokens = cache_read_tokens

    class CostMode:
        pass

# Hardcoded fallback pricing (USD per 1K tokens)
MODEL_PRICING = {
    "gpt-3.5-turbo": {
        "input": 0.0015,
        "output": 0.002,
        "cache_creation": 0.0005,
        "cache_read": 0.0001,
    },
    "gpt-4": {
        "input": 0.03,
        "output": 0.06,
        "cache_creation": 0.01,
        "cache_read": 0.002,
    },
    "default": {
        "input": 0.002,
        "output": 0.002,
        "cache_creation": 0.0005,
        "cache_read": 0.0001,
    }
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

    _pricing_cache_lock = threading.Lock()
    _pricing_cache = {}

    def __init__(self, custom_pricing: Optional[Dict[str, Dict[str, float]]] = None) -> None:
        '''Initialize with optional custom pricing.
        Args:
            custom_pricing: Optional custom pricing dictionary to override defaults.
                          Should follow same structure as MODEL_PRICING.
        '''
        self.custom_pricing = custom_pricing or {}

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
        # Use cache for pricing lookups
        cache_key = (id(self), model)
        with self._pricing_cache_lock:
            if cache_key in self._pricing_cache:
                return self._pricing_cache[cache_key]

        # 1. Try custom pricing
        if model in self.custom_pricing:
            pricing = self.custom_pricing[model]
        # 2. Try hardcoded pricing
        elif model in MODEL_PRICING:
            pricing = MODEL_PRICING[model]
        # 3. Try default fallback
        elif "default" in self.custom_pricing:
            pricing = self.custom_pricing["default"]
        elif "default" in MODEL_PRICING:
            pricing = MODEL_PRICING["default"]
        else:
            if strict:
                raise KeyError(f"Unknown model for pricing: {model}")
            pricing = {"input": 0.002, "output": 0.002,
                       "cache_creation": 0.0005, "cache_read": 0.0001}

        # Ensure all keys are present
        for k in ("input", "output", "cache_creation", "cache_read"):
            if k not in pricing:
                pricing[k] = 0.0

        with self._pricing_cache_lock:
            self._pricing_cache[cache_key] = pricing
        return pricing

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
        pricing = self._get_pricing_for_model(model, strict=strict)
        if tokens is not None:
            in_tokens = getattr(tokens, "input_tokens", 0)
            out_tokens = getattr(tokens, "output_tokens", 0)
            cache_create = getattr(tokens, "cache_creation_tokens", 0)
            cache_read = getattr(tokens, "cache_read_tokens", 0)
        else:
            in_tokens = input_tokens
            out_tokens = output_tokens
            cache_create = cache_creation_tokens
            cache_read = cache_read_tokens

        cost = (
            (in_tokens / 1000.0) * pricing["input"] +
            (out_tokens / 1000.0) * pricing["output"] +
            (cache_create / 1000.0) * pricing["cache_creation"] +
            (cache_read / 1000.0) * pricing["cache_read"]
        )
        return cost

    def calculate_cost_for_entry(self, entry_data: Dict[str, Any], mode: CostMode) -> float:
        '''Calculate cost for a single entry (backward compatibility).
        Args:
            entry_data: Entry data dictionary
            mode: Cost mode (for backward compatibility)
        Returns:
            Cost in USD
        '''
        # Try to extract model and token counts from entry_data
        model = entry_data.get("model") or entry_data.get(
            "model_name") or "default"
        # Try to extract tokens as a TokenCounts object or as fields
        tokens = entry_data.get("tokens")
        if tokens is not None and isinstance(tokens, TokenCounts):
            return self.calculate_cost(model, tokens=tokens)
        else:
            input_tokens = entry_data.get("input_tokens", 0)
            output_tokens = entry_data.get("output_tokens", 0)
            cache_creation_tokens = entry_data.get("cache_creation_tokens", 0)
            cache_read_tokens = entry_data.get("cache_read_tokens", 0)
            return self.calculate_cost(
                model,
                input_tokens=input_tokens,
                output_tokens=output_tokens,
                cache_creation_tokens=cache_creation_tokens,
                cache_read_tokens=cache_read_tokens
            )
