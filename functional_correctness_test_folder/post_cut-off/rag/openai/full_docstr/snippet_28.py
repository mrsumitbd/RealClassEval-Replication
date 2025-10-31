
from __future__ import annotations

from dataclasses import dataclass
from functools import lru_cache
from typing import Any, Dict, Optional

# --------------------------------------------------------------------------- #
#  Dummy / placeholder definitions – in a real project these would be imported
#  from the appropriate modules.  They are included here only so that the
#  implementation below can be executed in isolation.
# --------------------------------------------------------------------------- #

# Example default pricing – normally this would be imported from a config module
DEFAULT_MODEL_PRICING: Dict[str, Dict[str, float]] = {
    "gpt-4": {
        "input": 0.03,          # USD per 1K tokens
        "output": 0.06,
        "cache_creation": 0.01,
        "cache_read": 0.005,
    },
    "gpt-3.5-turbo": {
        "input": 0.0015,
        "output": 0.002,
        "cache_creation": 0.0005,
        "cache_read": 0.00025,
    },
}

# Simple dataclass for token counts – in practice this would be more elaborate


@dataclass(frozen=True)
class TokenCounts:
    input: int = 0
    output: int = 0
    cache_creation: int = 0
    cache_read: int = 0

# Cost mode enum – used only for backward‑compatibility


class CostMode:
    TOTAL = "total"
    INPUT = "input"
    OUTPUT = "output"
    CACHE = "cache"

# --------------------------------------------------------------------------- #
#  PricingCalculator implementation
# --------------------------------------------------------------------------- #


class PricingCalculator:
    """Calculates costs based on model pricing with caching support."""

    def __init__(
        self,
        custom_pricing: Optional[Dict[str, Dict[str, float]]] = None,
    ) -> None:
        """
        Initialize with optional custom pricing.

        Args:
            custom_pricing: Optional custom pricing dictionary to override defaults.
                            Should follow the same structure as DEFAULT_MODEL_PRICING.
        """
        # Merge custom pricing over defaults
        self._pricing: Dict[str, Dict[str, float]] = {
            model: dict(prices) for model, prices in DEFAULT_MODEL_PRICING.items()
        }
        if custom_pricing:
            for model, prices in custom_pricing.items():
                self._pricing[model] = dict(prices)

        # Cache for expensive look‑ups
        self._pricing_cache: Dict[str, Dict[str, float]] = {}

    # --------------------------------------------------------------------- #
    #  Public API
    # --------------------------------------------------------------------- #

    def calculate_cost(
        self,
        model: str,
        input_tokens: int = 0,
        output_tokens: int = 0,
        cache_creation_tokens: int = 0,
        cache_read_tokens: int = 0,
        tokens: Optional[TokenCounts] = None,
        strict: bool = False,
    ) -> float:
        """
        Calculate cost with flexible API supporting both signatures.

        Args:
            model: Model name
            input_tokens: Number of input tokens (ignored if tokens provided)
            output_tokens: Number of output tokens (ignored if tokens provided)
            cache_creation_tokens: Number of cache creation tokens
            cache_read_tokens: Number of cache read tokens
            tokens: Optional TokenCounts object (takes precedence)
            strict: If True, raise KeyError for unknown models

        Returns:
            Total cost in USD
        """
        if tokens is not None:
            input_tokens = tokens.input
            output_tokens = tokens.output
            cache_creation_tokens = tokens.cache_creation
            cache_read_tokens = tokens.cache_read

        # Use a cached helper to avoid recomputing the same cost
        return self._calculate_cost_cached(
            model,
            input_tokens,
            output_tokens,
            cache_creation_tokens,
            cache_read_tokens,
            strict,
        )

    def _get_pricing_for_model(
        self, model: str, strict: bool = False
    ) -> Dict[str, float]:
        """
        Get pricing for a model with optional fallback logic.

        Args:
            model: Model name
            strict: If True, raise KeyError for unknown models

        Returns:
            Pricing dictionary with input/output/cache costs

        Raises:
            KeyError: If strict=True and model is unknown
        """
        if model in self._pricing_cache:
            return self._pricing_cache[model]

        if model in self._pricing:
            pricing = self._pricing[model]
        else:
            if strict:
                raise KeyError(f"Unknown model '{model}'")
            # Fallback to a hard‑coded default if available
            pricing = DEFAULT_MODEL_PRICING.get(model, {})
            if not pricing:
                # If no pricing at all, assume zero cost
                pricing = {
                    "input": 0.0,
                    "output": 0.0,
                    "cache_creation": 0.0,
                    "cache_read": 0.0,
                }

        self._pricing_cache[model] = pricing
        return pricing

    def calculate_cost_for_entry(
        self, entry_data: Dict[str, Any], mode: CostMode
    ) -> float:
        """
        Calculate cost for a single entry (backward compatibility).

        Args:
            entry_data: Entry data dictionary
            mode: Cost mode (for backward compatibility)

        Returns:
            Cost in USD
        """
        model = entry_data.get("model")
        if not model:
            raise ValueError("Entry data must contain a 'model' key")

        # Extract token counts – support both legacy and new keys
        input_tokens = entry_data.get("input_tokens", 0)
        output_tokens = entry_data.get("output_tokens", 0)
        cache_creation_tokens = entry_data.get("cache_creation_tokens", 0)
        cache_read_tokens = entry_data.get("cache_read_tokens", 0)

        # If a TokenCounts object is present, use it
        tokens_obj = entry_data.get("tokens")
        if isinstance(tokens_obj, TokenCounts):
            input_tokens = tokens_obj.input
            output_tokens = tokens_obj.output
            cache_creation_tokens = tokens_obj.cache_creation
            cache_read_tokens = tokens_obj.cache_read

        # Compute the full cost first
        total_cost = self.calculate_cost(
            model,
            input_tokens=input_tokens,
            output_tokens=output_tokens,
            cache_creation_tokens=cache_creation_tokens,
            cache_read_tokens=cache_read_tokens,
            strict=False,
        )

        # If a specific mode is requested, compute only that part
        if mode == CostMode.TOTAL:
            return total_cost

        pricing = self._get_pricing_for_model(model, strict=False)

        if mode == CostMode.INPUT:
            return input_tokens * pricing.get("input", 0.0)
        if mode == CostMode.OUTPUT:
            return output_tokens * pricing.get("output", 0.0)
        if mode == CostMode.CACHE:
            cache_cost = (
                cache_creation_tokens * pricing.get("cache_creation", 0.0)
                + cache_read_tokens * pricing.get("cache_read", 0.0)
            )
            return cache_cost

        # Unknown mode – fall back to total
        return total_cost

    # --------------------------------------------------------------------- #
    #  Internal cached calculation
    # --------------------------------------------------------------------- #

    @lru_cache(maxsize=1024)
    def _calculate_cost_cached(
        self,
        model: str,
        input_tokens: int,
        output_tokens: int,
        cache_creation_tokens: int,
        cache_read_tokens: int,
        strict: bool,
    ) -> float:
        """
        Cached helper that performs the actual cost calculation.
        """
        pricing = self._get_pricing_for_model(model, strict=strict)

        # Prices are per 1K tokens – convert to per token
        input_price = pricing.get("input", 0.0
