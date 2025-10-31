
from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Any, Dict, Optional

# Simple token counts container
TokenCounts = Dict[str, int]


class CostMode(Enum):
    INPUT = "input"
    OUTPUT = "output"
    CACHE_CREATION = "cache_creation"
    CACHE_READ = "cache_read"
    ALL = "all"


class PricingCalculator:
    """
    A simple pricing calculator that supports custom pricing per model.
    """

    # Default pricing per token (USD)
    _DEFAULT_PRICING: Dict[str, float] = {
        "input": 0.0004,
        "output": 0.0004,
        "cache_creation": 0.0004,
        "cache_read": 0.0004,
    }

    def __init__(
        self,
        custom_pricing: Optional[Dict[str, Dict[str, float]]] = None,
    ) -> None:
        """
        Parameters
        ----------
        custom_pricing : Optional[Dict[str, Dict[str, float]]]
            Mapping from model name to a pricing dictionary. Each pricing
            dictionary may contain any of the keys in `_DEFAULT_PRICING`.
        """
        self.custom_pricing = custom_pricing or {}

    def _get_pricing_for_model(
        self, model: str, strict: bool = False
    ) -> Dict[str, float]:
        """
        Retrieve the pricing dictionary for a given model.

        Parameters
        ----------
        model : str
            The model name.
        strict : bool
            If True, raise a ValueError when the model is not found.

        Returns
        -------
        Dict[str, float]
            The pricing dictionary for the model.
        """
        if model in self.custom_pricing:
            pricing = self.custom_pricing[model]
        else:
            if strict:
                raise ValueError(f"Pricing for model '{model}' not found.")
            pricing = {}

        # Merge with defaults
        merged = self._DEFAULT_PRICING.copy()
        merged.update(pricing)
        return merged

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
        Calculate the total cost for a request.

        Parameters
        ----------
        model : str
            The model name.
        input_tokens : int
            Number of input tokens.
        output_tokens : int
            Number of output tokens.
        cache_creation_tokens : int
            Number of cache creation tokens.
        cache_read_tokens : int
            Number of cache read tokens.
        tokens : Optional[TokenCounts]
            Alternative way to provide token counts as a dictionary.
        strict : bool
            If True, raise an error when the model is not found.

        Returns
        -------
        float
            The total cost in USD.
        """
        pricing = self._get_pricing_for_model(model, strict=strict)

        if tokens is not None:
            input_tokens = tokens.get("input", input_tokens)
            output_tokens = tokens.get("output", output_tokens)
            cache_creation_tokens = tokens.get(
                "cache_creation", cache_creation_tokens)
            cache_read_tokens = tokens.get("cache_read", cache_read_tokens)

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
        Calculate the cost for a single entry dictionary.

        Parameters
        ----------
        entry_data : Dict[str, Any]
            Dictionary containing at least the keys:
                - "model": str
                - "input_tokens": int
                - "output_tokens": int
                - "cache_creation_tokens": int
                - "cache_read_tokens": int
        mode : CostMode
            Which part of the cost to calculate.

        Returns
        -------
        float
            The calculated cost in USD.
        """
        model = entry_data.get("model")
        if not model:
            raise ValueError("Entry data must contain a 'model' key.")

        # Extract token counts with defaults
        input_tokens = entry_data.get("input_tokens", 0)
        output_tokens = entry_data.get("output_tokens", 0)
        cache_creation_tokens = entry_data.get("cache_creation_tokens", 0)
        cache_read_tokens = entry_data.get("cache_read_tokens", 0)

        pricing = self._get_pricing_for_model(model)

        if mode == CostMode.INPUT:
            return input_tokens * pricing["input"]
        if mode == CostMode.OUTPUT:
            return output_tokens * pricing["output"]
        if mode == CostMode.CACHE_CREATION:
            return cache_creation_tokens * pricing["cache_creation"]
        if mode == CostMode.CACHE_READ:
            return cache_read_tokens * pricing["cache_read"]
        if mode == CostMode.ALL:
            return self.calculate_cost(
                model,
                input_tokens=input_tokens,
                output_tokens=output_tokens,
                cache_creation_tokens=cache_creation_tokens,
                cache_read_tokens=cache_read_tokens,
            )

        raise ValueError(f"Unsupported CostMode: {mode}")
