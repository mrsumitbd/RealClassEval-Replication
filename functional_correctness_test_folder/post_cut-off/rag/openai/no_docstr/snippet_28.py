
from __future__ import annotations

from typing import Any, Dict, Optional, Tuple

# The following imports are expected to exist in the package that uses this
# class.  They are imported lazily to avoid circular dependencies.
try:
    from .pricing import MODEL_PRICING  # type: ignore
except Exception:  # pragma: no cover
    # Fallback hard‑coded pricing if the module is not available.
    MODEL_PRICING: Dict[str, Dict[str, float]] = {
        "gpt-4": {"input": 0.03, "output": 0.06, "cache_creation": 0.01, "cache_read": 0.005},
        "gpt-3.5-turbo": {"input": 0.0015, "output": 0.002, "cache_creation": 0.0005, "cache_read": 0.00025},
    }

# TokenCounts and CostMode are simple data structures used by the API.
# If they are not defined elsewhere, we provide minimal stubs.
try:
    from .types import TokenCounts, CostMode  # type: ignore
except Exception:  # pragma: no cover
    class TokenCounts:
        def __init__(
            self,
            input: int = 0,
            output: int = 0,
            cache_creation: int = 0,
            cache_read: int = 0,
        ):
            self.input = input
            self.output = output
            self.cache_creation = cache_creation
            self.cache_read = cache_read

    class CostMode:
        FULL = "full"
        INPUT_ONLY = "input_only"
        OUTPUT_ONLY = "output_only"


class PricingCalculator:
    """Calculates costs based on model pricing with caching support.

    This class provides methods for calculating costs for individual models/tokens
    as well as detailed cost breakdowns for collections of usage entries.
    It supports custom pricing configurations and caches calculations for performance.
    """

    def __init__(
        self,
        custom_pricing: Optional[Dict[str, Dict[str, float]]] = None,
    ) -> None:
        """Initialize with optional custom pricing.

        Args:
            custom_pricing: Optional custom pricing dictionary to override defaults.
                            Should follow same structure as MODEL_PRICING.
        """
        # Merge custom pricing into the default pricing dictionary.
        self._pricing: Dict[str, Dict[str, float]] = dict(MODEL_PRICING)
        if custom_pricing:
            for model, prices in custom_pricing.items():
                self._pricing[model] = dict(prices)

        # Simple LRU‑style cache for cost calculations.
        self._cache: Dict[Tuple[Any, ...], float] = {}

    def _get_pricing_for_model(
        self, model: str, strict: bool = False
    ) -> Dict[str, float]:
        """Get pricing for a model with optional fallback logic.

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
        # Fallback to an empty pricing dict (all costs zero)
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

        # Cache key includes all parameters that influence the result.
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

    def calculate_cost_for_entry(
        self, entry_data: Dict[str, Any], mode: CostMode
    ) -> float:
        """Calculate cost for a single entry (backward compatibility).

        Args:
            entry_data: Entry data dictionary
            mode: Cost mode (for backward compatibility)

        Returns:
            Cost in USD
        """
        # The entry_data may contain either a 'tokens' key or individual token counts.
        if "tokens" in entry_data:
            tokens = entry_data["tokens"]
            if not isinstance(tokens, TokenCounts):
                # If a plain dict is provided, convert it.
                tokens = TokenCounts(
                    input=tokens.get("input", 0),
                    output=tokens.get("output", 0),
                    cache_creation=tokens.get("cache_creation", 0),
                    cache_read=tokens.get("cache_read", 0),
                )
            return self.calculate_cost(
                model=entry_data["model"],
                tokens=tokens,
                strict=False,
            )

        # Fallback to individual fields
        return self.calculate_cost(
            model=entry_data["model"],
            input_tokens=entry_data.get("input_tokens", 0),
            output_tokens=entry_data.get("output_tokens", 0),
            cache_creation_tokens=entry_data.get("cache_creation_tokens", 0),
            cache_read_tokens=entry_data.get("cache_read_tokens", 0),
            strict=False,
        )
