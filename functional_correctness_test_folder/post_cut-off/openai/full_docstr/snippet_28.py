
from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from functools import lru_cache
from typing import Any, Dict, Optional

# --------------------------------------------------------------------------- #
# Basic data structures and defaults
# --------------------------------------------------------------------------- #


class CostMode(Enum):
    INPUT = "input"
    OUTPUT = "output"
    CACHE_CREATION = "cache_creation"
    CACHE_READ = "cache_read"
    TOTAL = "total"


@dataclass
class TokenCounts:
    input: int = 0
    output: int = 0
    cache_creation: int = 0
    cache_read: int = 0


# Default hard‑coded pricing (per token, USD)
DEFAULT_PRICING: Dict[str, Dict[str, float]] = {
    "gpt-4o-mini": {
        "input": 0.0004,
        "output": 0.0016,
        "cache_creation": 0.0004,
        "cache_read": 0.0004,
    },
    "gpt-4o": {
        "input": 0.0005,
        "output": 0.0020,
        "cache_creation": 0.0005,
        "cache_read": 0.0005,
    },
    # Add more models as needed
}


# --------------------------------------------------------------------------- #
# PricingCalculator implementation
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
                            Should follow the same structure as DEFAULT_PRICING.
        """
        # Merge custom pricing into defaults; custom values override defaults
        self._pricing: Dict[str, Dict[str, float]] = {
            model: dict(prices) for model, prices in DEFAULT_PRICING.items()
        }
        if custom_pricing:
            for model, prices in custom_pricing.items():
                self._pricing[model] = dict(prices)

    # --------------------------------------------------------------------- #
    # Internal helpers
    # --------------------------------------------------------------------- #

    @lru_cache(maxsize=128)
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
            raise KeyError(f"Pricing for model '{model}' not found.")
        # Fallback to a generic default if model unknown
        return {
            "input": 0.0004,
            "output": 0.0016,
            "cache_creation": 0.0004,
            "cache_read": 0.0004,
        }

    # --------------------------------------------------------------------- #
    # Public API
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

        pricing = self._get_pricing_for_model(model, strict=strict)

        cost = (
            input_tokens * pricing["input"]
            + output_tokens * pricing["output"]
            + cache_creation_tokens * pricing["cache_creation"]
            + cache_read_tokens * pricing["cache_read"]
        )
        return cost

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
            raise ValueError("Entry data must contain a 'model' key.")

        # Extract token counts; fall back to 0 if missing
        input_tokens = int(entry_data.get("input_tokens", 0))
        output_tokens = int(entry_data.get("output_tokens", 0))
        cache_creation_tokens = int(entry_data.get("cache_creation_tokens", 0))
        cache_read_tokens = int(entry_data.get("cache_read_tokens", 0))

        if mode == CostMode.TOTAL:
            return self.calculate_cost(
                model,
                input_tokens=input_tokens,
                output_tokens=output_tokens,
                cache_creation_tokens=cache_creation_tokens,
                cache_read_tokens=cache_read_tokens,
            )
        # For individual modes, compute only the relevant part
        pricing = self._get_pricing_for_model(model)
        if mode == CostMode.INPUT:
            return input_tokens * pricing["input"]
        if mode == CostMode.OUTPUT:
            return output_tokens * pricing["output"]
        if mode == CostMode.CACHE_CREATION:
            return cache_creation_tokens * pricing["cache_creation"]
        if mode == CostMode.CACHE_READ:
            return cache_read_tokens * pricing["cache_read"]

        raise ValueError(f"Unsupported CostMode: {mode}")
