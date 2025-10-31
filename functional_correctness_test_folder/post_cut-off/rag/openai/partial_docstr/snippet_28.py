
from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, Optional, Tuple

# --------------------------------------------------------------------------- #
#  Dummy definitions for the types that are referenced in the skeleton.
#  In a real project these would be imported from the appropriate modules.
# --------------------------------------------------------------------------- #

# A minimal TokenCounts representation


@dataclass(frozen=True)
class TokenCounts:
    input: int = 0
    output: int = 0
    cache_creation: int = 0
    cache_read: int = 0

# A minimal CostMode enum (only used for backward‑compatibility)


class CostMode:
    INPUT = "input"
    OUTPUT = "output"
    CACHE = "cache"

# --------------------------------------------------------------------------- #
#  Default pricing table (hard‑coded fallback)
# --------------------------------------------------------------------------- #


DEFAULT_MODEL_PRICING: Dict[str, Dict[str, float]] = {
    "gpt-4": {
        "input": 0.03 / 1000,
        "output": 0.06 / 1000,
        "cache_creation": 0.01 / 1000,
        "cache_read": 0.005 / 1000,
    },
    "gpt-3.5-turbo": {
        "input": 0.0015 / 1000,
        "output": 0.002 / 1000,
        "cache_creation": 0.0005 / 1000,
        "cache_read": 0.00025 / 1000,
    },
    # Add more models as needed
}

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
        # Merge custom pricing into the default table
        self._pricing: Dict[str, Dict[str, float]] = {
            model: dict(prices) for model, prices in DEFAULT_MODEL_PRICING.items()
        }
        if custom_pricing:
            for model, prices in custom_pricing.items():
                self._pricing[model] = dict(prices)

        # Simple cache: key -> cost
        self._cache: Dict[Tuple, float] = {}

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
        # Resolve token counts
        if tokens is not None:
            input_t = tokens.input
            output_t = tokens.output
            cache_creation_t = tokens.cache_creation
            cache_read_t = tokens.cache_read
        else:
            input_t = input_tokens
            output_t = output_tokens
            cache_creation_t = cache_creation_tokens
            cache_read_t = cache_read_tokens

        # Build cache key
        key = (
            model,
            input_t,
            output_t,
            cache_creation_t,
            cache_read_t,
            strict,
        )
        if key in self._cache:
            return self._cache[key]

        pricing = self._get_pricing_for_model(model, strict=strict)

        cost = (
            input_t * pricing.get("input", 0.0)
            + output_t * pricing.get("output", 0.0)
            + cache_creation_t * pricing.get("cache_creation", 0.0)
            + cache_read_t * pricing.get("cache_read", 0.0)
        )

        self._cache[key] = cost
        return cost

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
        if model in self._pricing:
            return self._pricing[model]
        if strict:
            raise KeyError(f"Unknown model '{model}'")
        # Fallback: zero pricing
        return {
            "input": 0.0,
            "output": 0.0,
            "cache_creation": 0.0,
            "cache_read": 0.0,
        }

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
        # Extract fields with defaults
        model = entry_data.get("model", "")
        input_t = entry_data.get("input_tokens", 0)
        output_t = entry_data.get("output_tokens", 0)
        cache_creation_t = entry_data.get("cache_creation_tokens", 0)
        cache_read_t = entry_data.get("cache_read_tokens", 0)

        # The `mode` argument is ignored in the new API but kept for
        # backward compatibility.  It can be used to enforce strictness
        # if desired.
        strict = mode == CostMode.CACHE  # arbitrary example

        return self.calculate_cost(
            model,
            input_tokens=input_t,
            output_tokens=output_t,
            cache_creation_tokens=cache_creation_t,
            cache_read_tokens=cache_read_t,
            strict=strict,
        )
