
from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Any, Dict, Optional

# --------------------------------------------------------------------------- #
# Helper types and defaults
# --------------------------------------------------------------------------- #


class CostMode(Enum):
    """Backward‑compatibility cost modes."""
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


# Default pricing for a few example models (USD per token)
DEFAULT_MODEL_PRICING: Dict[str, Dict[str, float]] = {
    "gpt-4": {
        "input": 0.03 / 1000,
        "output": 0.06 / 1000,
        "cache_creation": 0.02 / 1000,
        "cache_read": 0.01 / 1000,
    },
    "gpt-3.5-turbo": {
        "input": 0.0015 / 1000,
        "output": 0.002 / 1000,
        "cache_creation": 0.001 / 1000,
        "cache_read": 0.0005 / 1000,
    },
    # Add more models as needed
}


# --------------------------------------------------------------------------- #
# PricingCalculator implementation
# --------------------------------------------------------------------------- #

class PricingCalculator:
    def __init__(
        self,
        custom_pricing: Optional[Dict[str, Dict[str, float]]] = None,
    ) -> None:
        """
        Initialize with optional custom pricing.
        Args:
            custom_pricing: Optional custom pricing dictionary to override defaults.
                            Should follow same structure as DEFAULT_MODEL_PRICING.
        """
        self._custom_pricing = custom_pricing or {}
        # Merge custom pricing into defaults; custom values override defaults
        self._pricing = {
            model: {
                **DEFAULT_MODEL_PRICING.get(model, {}), **self._custom_pricing.get(model, {})}
            for model in set(DEFAULT_MODEL_PRICING) | set(self._custom_pricing)
        }

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
        # Return zero pricing if not strict
        return {"input": 0.0, "output": 0.0, "cache_creation": 0.0, "cache_read": 0.0}

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
        Returns:
            Total cost in USD
        """
        pricing = self._get_pricing_for_model(model, strict=strict)

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

        cost = (
            input_t * pricing.get("input", 0.0)
            + output_t * pricing.get("output", 0.0)
            + cache_creation_t * pricing.get("cache_creation", 0.0)
            + cache_read_t * pricing.get("cache_read", 0.0)
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

        pricing = self._get_pricing_for_model(model, strict=False)

        # Extract token counts from entry_data; default to 0 if missing
        input_t = int(entry_data.get("input_tokens", 0))
        output_t = int(entry_data.get("output_tokens", 0))
        cache_creation_t = int(entry_data.get("cache_creation_tokens", 0))
        cache_read_t = int(entry_data.get("cache_read_tokens", 0))

        if mode == CostMode.INPUT:
            return input_t * pricing.get("input", 0.0)
        if mode == CostMode.OUTPUT:
            return output_t * pricing.get("output", 0.0)
        if mode == CostMode.CACHE_CREATION:
            return cache_creation_t * pricing.get("cache_creation", 0.0)
        if mode == CostMode.CACHE_READ:
            return cache_read_t * pricing.get("cache_read", 0.0)
        if mode == CostMode.TOTAL:
            return (
                input_t * pricing.get("input", 0.0)
                + output_t * pricing.get("output", 0.0)
                + cache_creation_t * pricing.get("cache_creation", 0.0)
                + cache_read_t * pricing.get("cache_read", 0.0)
            )

        raise ValueError(f"Unsupported cost mode: {mode}")
