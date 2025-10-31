from __future__ import annotations

from typing import Optional, Dict, Any, Tuple


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

    # Prices are USD per 1K tokens
    DEFAULT_MODEL_PRICING: Dict[str, Dict[str, float]] = {
        # OpenAI common models (as of mid-2024, approximate/fallback values)
        "gpt-4o": {"input": 0.005, "output": 0.015, "cache_creation": 0.0, "cache_read": 0.0},
        "gpt-4o-mini": {"input": 0.00015, "output": 0.0006, "cache_creation": 0.0, "cache_read": 0.0},
        "gpt-4-turbo": {"input": 0.01, "output": 0.03, "cache_creation": 0.0, "cache_read": 0.0},
        "gpt-4": {"input": 0.03, "output": 0.06, "cache_creation": 0.0, "cache_read": 0.0},
        "gpt-3.5-turbo": {"input": 0.0005, "output": 0.0015, "cache_creation": 0.0, "cache_read": 0.0},
        # Sensible generic fallback
        "default": {"input": 0.0005, "output": 0.0015, "cache_creation": 0.0, "cache_read": 0.0},
    }

    def __init__(self, custom_pricing: Optional[Dict[str, Dict[str, float]]] = None) -> None:
        '''Initialize with optional custom pricing.
        Args:
            custom_pricing: Optional custom pricing dictionary to override defaults.
                          Should follow same structure as MODEL_PRICING.
        '''
        self._pricing = dict(self.DEFAULT_MODEL_PRICING)
        if custom_pricing:
            # Normalize keys and merge (custom overrides defaults)
            normalized = {self._normalize_model_name(
                k): v for k, v in custom_pricing.items()}
            self._pricing.update(normalized)

        # Caches
        self._model_pricing_cache: Dict[str, Dict[str, float]] = {}
        self._cost_cache: Dict[Tuple[str, int, int, int, int], float] = {}

    def calculate_cost(self, model: str, input_tokens: int = 0, output_tokens: int = 0, cache_creation_tokens: int = 0, cache_read_tokens: int = 0, tokens: Optional[Any] = None, strict: bool = False) -> float:
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
            # Extract from TokenCounts-like object (dict or attrs)
            input_tokens = self._get_field(
                tokens, ("input_tokens", "prompt_tokens", "input", "prompt"), 0)
            output_tokens = self._get_field(
                tokens, ("output_tokens", "completion_tokens", "output", "completion"), 0)
            cache_creation_tokens = self._get_field(
                tokens, ("cache_creation_tokens", "cache_write_tokens", "cache_write_input_tokens", "cache_creation", "cache_write"), 0)
            cache_read_tokens = self._get_field(
                tokens, ("cache_read_tokens", "cache_read_input_tokens", "cache_read"), 0)

        normalized_model = self._normalize_model_name(model)
        cache_key = (normalized_model, int(input_tokens), int(
            output_tokens), int(cache_creation_tokens), int(cache_read_tokens))
        if cache_key in self._cost_cache:
            return self._cost_cache[cache_key]

        pricing = self._get_pricing_for_model(model, strict=strict)
        # Per 1K tokens pricing
        input_cost = (input_tokens / 1000.0) * pricing.get("input", 0.0)
        output_cost = (output_tokens / 1000.0) * pricing.get("output", 0.0)
        cache_create_cost = (cache_creation_tokens / 1000.0) * pricing.get(
            "cache_creation", pricing.get("input", 0.0) if "cache_creation" not in pricing else 0.0)
        cache_read_cost = (cache_read_tokens / 1000.0) * \
            pricing.get("cache_read", 0.0)

        total = input_cost + output_cost + cache_create_cost + cache_read_cost
        self._cost_cache[cache_key] = total
        return total

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
        normalized = self._normalize_model_name(model)
        if normalized in self._model_pricing_cache:
            return self._model_pricing_cache[normalized]

        # Exact match in configured pricing
        if normalized in self._pricing:
            pricing = self._complete_pricing(self._pricing[normalized])
            self._model_pricing_cache[normalized] = pricing
            return pricing

        # Heuristic aliasing for common variants
        aliases = self._aliases_for(normalized)
        for alias in aliases:
            if alias in self._pricing:
                pricing = self._complete_pricing(self._pricing[alias])
                self._model_pricing_cache[normalized] = pricing
                return pricing

        if strict:
            raise KeyError(f"Unknown model for pricing: {model}")

        # Fallback to default
        pricing = self._complete_pricing(self._pricing.get(
            "default", {"input": 0.0, "output": 0.0, "cache_creation": 0.0, "cache_read": 0.0}))
        self._model_pricing_cache[normalized] = pricing
        return pricing

    def calculate_cost_for_entry(self, entry_data: Dict[str, Any], mode: Any) -> float:
        '''Calculate cost for a single entry (backward compatibility).
        Args:
            entry_data: Entry data dictionary
            mode: Cost mode (for backward compatibility)
        Returns:
            Cost in USD
        '''
        model = entry_data.get("model") or entry_data.get(
            "name") or entry_data.get("engine") or "default"

        # Typical shapes:
        # - entry_data["usage"] dict with prompt_tokens, completion_tokens, etc.
        # - tokens at top-level
        usage = entry_data.get("usage") or {}

        def g(d: Dict[str, Any], keys: Tuple[str, ...], default: int = 0) -> int:
            for k in keys:
                if k in d and d[k] is not None:
                    try:
                        return int(d[k])
                    except Exception:
                        pass
            return default

        # Collect tokens with a broad compatibility set of keys
        input_tokens = g(usage, ("input_tokens", "prompt_tokens",
                         "tokens_input", "input", "prompt"))
        output_tokens = g(usage, ("output_tokens", "completion_tokens",
                          "tokens_output", "output", "completion"))
        cache_creation_tokens = g(usage, ("cache_creation_tokens", "cache_write_tokens",
                                  "cache_write_input_tokens", "cache_creation", "cache_write"))
        cache_read_tokens = g(
            usage, ("cache_read_tokens", "cache_read_input_tokens", "cache_read"))

        # Also consider top-level keys if not present in usage
        if input_tokens == 0:
            input_tokens = g(entry_data, ("input_tokens",
                             "prompt_tokens", "tokens_input", "input", "prompt"))
        if output_tokens == 0:
            output_tokens = g(entry_data, ("output_tokens",
                              "completion_tokens", "tokens_output", "output", "completion"))
        if cache_creation_tokens == 0:
            cache_creation_tokens = g(entry_data, ("cache_creation_tokens", "cache_write_tokens",
                                      "cache_write_input_tokens", "cache_creation", "cache_write"))
        if cache_read_tokens == 0:
            cache_read_tokens = g(
                entry_data, ("cache_read_tokens", "cache_read_input_tokens", "cache_read"))

        return self.calculate_cost(
            model=model,
            input_tokens=input_tokens,
            output_tokens=output_tokens,
            cache_creation_tokens=cache_creation_tokens,
            cache_read_tokens=cache_read_tokens,
        )

    # -----------------
    # Internal helpers
    # -----------------
    @staticmethod
    def _normalize_model_name(model: str) -> str:
        m = (model or "").strip().lower()
        if "/" in m:
            m = m.split("/")[-1]

        # Collapse known dated suffixes or variants to base family where reasonable
        # Examples: gpt-4o-2024-08-06 -> gpt-4o
        for base in ("gpt-4o-mini", "gpt-4o", "gpt-4-turbo", "gpt-4", "gpt-3.5-turbo"):
            if m == base or m.startswith(base + "-"):
                return base

        return m

    @staticmethod
    def _aliases_for(normalized: str) -> Tuple[str, ...]:
        # Common family aliasing
        if normalized.startswith("gpt-4o-"):
            return ("gpt-4o",)
        if normalized.startswith("gpt-4o-mini-"):
            return ("gpt-4o-mini",)
        if normalized.startswith("gpt-4-"):
            return ("gpt-4-turbo", "gpt-4")
        if normalized.startswith("gpt-3.5-"):
            return ("gpt-3.5-turbo",)
        return ("default",)

    @staticmethod
    def _complete_pricing(pr: Dict[str, float]) -> Dict[str, float]:
        # Ensure all fields are present; default cache costs to 0.0 if unspecified
        return {
            "input": float(pr.get("input", 0.0)),
            "output": float(pr.get("output", 0.0)),
            "cache_creation": float(pr.get("cache_creation", 0.0)),
            "cache_read": float(pr.get("cache_read", 0.0)),
        }

    @staticmethod
    def _get_field(obj: Any, names: Tuple[str, ...], default: int = 0) -> int:
        for name in names:
            # attribute
            if hasattr(obj, name):
                val = getattr(obj, name)
                if val is not None:
                    try:
                        return int(val)
                    except Exception:
                        pass
            # mapping
            if isinstance(obj, dict) and name in obj and obj[name] is not None:
                try:
                    return int(obj[name])
                except Exception:
                    pass
        return default
