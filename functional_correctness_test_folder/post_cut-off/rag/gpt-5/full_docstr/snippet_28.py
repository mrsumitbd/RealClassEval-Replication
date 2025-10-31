from __future__ import annotations

from typing import Optional, Dict, Any, Mapping, Tuple


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

    # Base fallback pricing in USD per 1K tokens
    _DEFAULT_MODEL_PRICING: Dict[str, Dict[str, float]] = {
        # Generic default
        "default": {
            "input": 0.0010,
            "output": 0.0020,
            "cache_creation": 0.0010,
            "cache_read": 0.0005,
        },
        # Common OpenAI-like models (approximate defaults for robustness)
        "gpt-3.5-turbo": {
            "input": 0.0015,
            "output": 0.0020,
            "cache_creation": 0.0015,
            "cache_read": 0.0005,
        },
        "gpt-4o-mini": {
            "input": 0.0003,
            "output": 0.0012,
            "cache_creation": 0.0003,
            "cache_read": 0.0001,
        },
        "gpt-4o": {
            "input": 0.0050,
            "output": 0.0150,
            "cache_creation": 0.0050,
            "cache_read": 0.0010,
        },
        "gpt-4.1": {
            "input": 0.0050,
            "output": 0.0150,
            "cache_creation": 0.0050,
            "cache_read": 0.0010,
        },
        # Anthropic-like
        "claude-3-5-sonnet": {
            "input": 0.0030,
            "output": 0.0150,
            "cache_creation": 0.0030,
            "cache_read": 0.0010,
        },
        "claude-3-5-haiku": {
            "input": 0.0008,
            "output": 0.0040,
            "cache_creation": 0.0008,
            "cache_read": 0.0003,
        },
        # Google-like
        "gemini-1.5-flash": {
            "input": 0.00035,
            "output": 0.00105,
            "cache_creation": 0.00035,
            "cache_read": 0.00015,
        },
        "gemini-1.5-pro": {
            "input": 0.0035,
            "output": 0.0105,
            "cache_creation": 0.0035,
            "cache_read": 0.0015,
        },
        # O-series (approx)
        "o3-mini": {
            "input": 0.0006,
            "output": 0.0024,
            "cache_creation": 0.0006,
            "cache_read": 0.0002,
        },
        "o4-mini": {
            "input": 0.0008,
            "output": 0.0032,
            "cache_creation": 0.0008,
            "cache_read": 0.0003,
        },
    }

    def __init__(self, custom_pricing: Optional[Dict[str, Dict[str, float]]] = None) -> None:
        '''Initialize with optional custom pricing.
        Args:
            custom_pricing: Optional custom pricing dictionary to override defaults.
                          Should follow same structure as MODEL_PRICING.
        '''
        # Normalize base pricing to ensure all fields exist
        self._pricing: Dict[str, Dict[str, float]] = {}
        for name, cfg in self._DEFAULT_MODEL_PRICING.items():
            self._pricing[name.lower()] = self._normalize_pricing(cfg)

        # Apply custom overrides if provided
        if custom_pricing:
            for name, cfg in custom_pricing.items():
                self._pricing[name.lower()] = self._normalize_pricing(cfg)

        # Cache for resolved model pricing lookups (prefix matching)
        self._model_pricing_cache: Dict[str, Dict[str, float]] = {}
        # Cache for computed costs keyed by (model, input, output, cache_create, cache_read, version)
        self._calc_cache: Dict[Tuple[str, int, int, int, int], float] = {}

    def _normalize_pricing(self, cfg: Mapping[str, float]) -> Dict[str, float]:
        # Ensure all keys present; default to 0.0 if missing
        return {
            "input": float(cfg.get("input", 0.0)),
            "output": float(cfg.get("output", 0.0)),
            "cache_creation": float(cfg.get("cache_creation", cfg.get("cache_write", 0.0))),
            "cache_read": float(cfg.get("cache_read", 0.0)),
        }

    def _normalize_token_counts(
        self,
        input_tokens: int = 0,
        output_tokens: int = 0,
        cache_creation_tokens: int = 0,
        cache_read_tokens: int = 0,
        tokens: Optional["TokenCounts"] = None,
    ) -> Tuple[int, int, int, int]:
        if tokens is not None:
            # Attempt attribute access first
            get = lambda obj, *names: next(
                (int(getattr(obj, n)) for n in names if hasattr(obj, n)),
                None
            )
            in_val = get(tokens, "input_tokens", "prompt_tokens", "input")
            out_val = get(tokens, "output_tokens",
                          "completion_tokens", "output")
            cc_val = get(tokens, "cache_creation_tokens",
                         "cache_write_tokens", "cache_create_tokens", "cache_creation")
            cr_val = get(tokens, "cache_read_tokens", "cache_read")

            # Fallback to mapping-style access if needed
            if in_val is None and isinstance(tokens, Mapping):
                in_val = next((int(tokens[k]) for k in (
                    "input_tokens", "prompt_tokens", "input") if k in tokens), 0)
            if out_val is None and isinstance(tokens, Mapping):
                out_val = next((int(tokens[k]) for k in (
                    "output_tokens", "completion_tokens", "output") if k in tokens), 0)
            if cc_val is None and isinstance(tokens, Mapping):
                cc_val = next((int(tokens[k]) for k in (
                    "cache_creation_tokens", "cache_write_tokens", "cache_create_tokens", "cache_creation") if k in tokens), 0)
            if cr_val is None and isinstance(tokens, Mapping):
                cr_val = next((int(tokens[k]) for k in (
                    "cache_read_tokens", "cache_read") if k in tokens), 0)

            input_tokens = in_val if in_val is not None else 0
            output_tokens = out_val if out_val is not None else 0
            cache_creation_tokens = cc_val if cc_val is not None else 0
            cache_read_tokens = cr_val if cr_val is not None else 0

        # Sanitize and ensure non-negative ints
        def clamp_int(v: Any) -> int:
            try:
                iv = int(v)
            except Exception:
                iv = 0
            return iv if iv >= 0 else 0

        return (
            clamp_int(input_tokens),
            clamp_int(output_tokens),
            clamp_int(cache_creation_tokens),
            clamp_int(cache_read_tokens),
        )

    def calculate_cost(self, model: str, input_tokens: int = 0, output_tokens: int = 0, cache_creation_tokens: int = 0, cache_read_tokens: int = 0, tokens: Optional["TokenCounts"] = None, strict: bool = False) -> float:
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
        in_tok, out_tok, cc_tok, cr_tok = self._normalize_token_counts(
            input_tokens, output_tokens, cache_creation_tokens, cache_read_tokens, tokens
        )

        model_key = (model or "").strip()
        pricing = self._get_pricing_for_model(model_key, strict=strict)

        cache_key = (model_key.lower(), in_tok, out_tok, cc_tok, cr_tok)
        if cache_key in self._calc_cache:
            return self._calc_cache[cache_key]

        cost = (
            (in_tok * pricing["input"])
            + (out_tok * pricing["output"])
            + (cc_tok * pricing["cache_creation"])
            + (cr_tok * pricing["cache_read"])
        ) / 1000.0

        self._calc_cache[cache_key] = cost
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
        key = model.lower().strip()

        if key in self._model_pricing_cache:
            return self._model_pricing_cache[key]

        if key in self._pricing:
            pricing = self._pricing[key]
            self._model_pricing_cache[key] = pricing
            return pricing

        # Attempt longest-prefix match
        best_match = ""
        best_cfg = None
        for name, cfg in self._pricing.items():
            if key.startswith(name) and len(name) > len(best_match):
                best_match = name
                best_cfg = cfg

        if best_cfg is not None:
            self._model_pricing_cache[key] = best_cfg
            return best_cfg

        if strict:
            raise KeyError(f"Unknown model pricing for '{model}'")

        # Fallback to default
        default_cfg = self._pricing.get(
            "default", {"input": 0.0, "output": 0.0, "cache_creation": 0.0, "cache_read": 0.0})
        self._model_pricing_cache[key] = default_cfg
        return default_cfg

    def calculate_cost_for_entry(self, entry_data: Dict[str, Any], mode: "CostMode") -> float:
        '''Calculate cost for a single entry (backward compatibility).
        Args:
            entry_data: Entry data dictionary
            mode: Cost mode (for backward compatibility)
        Returns:
            Cost in USD
        '''
        # Extract model name
        model = (
            entry_data.get("model")
            or entry_data.get("model_name")
            or entry_data.get("name")
            or ""
        )

        # Find usage sub-dict if present
        usage = entry_data.get("usage")
        if usage is None and "response" in entry_data and isinstance(entry_data["response"], Mapping):
            usage = entry_data["response"].get("usage")

        # Token counts
        def pick(mapping: Mapping[str, Any], keys: Tuple[str, ...], default: int = 0) -> int:
            for k in keys:
                if k in mapping:
                    try:
                        return int(mapping[k])
                    except Exception:
                        return default
            return default

        if isinstance(usage, Mapping):
            input_tokens = pick(
                usage, ("input_tokens", "prompt_tokens", "input"), 0)
            output_tokens = pick(
                usage, ("output_tokens", "completion_tokens", "output"), 0)
            cache_creation_tokens = pick(
                usage, ("cache_creation_tokens", "cache_write_tokens", "cache_create_tokens", "cache_creation"), 0)
            cache_read_tokens = pick(
                usage, ("cache_read_tokens", "cache_read"), 0)
        else:
            input_tokens = pick(
                entry_data, ("input_tokens", "prompt_tokens", "input"), 0)
            output_tokens = pick(
                entry_data, ("output_tokens", "completion_tokens", "output"), 0)
            cache_creation_tokens = pick(
                entry_data, ("cache_creation_tokens", "cache_write_tokens", "cache_create_tokens", "cache_creation"), 0)
            cache_read_tokens = pick(
                entry_data, ("cache_read_tokens", "cache_read"), 0)

        return self.calculate_cost(
            model=model,
            input_tokens=input_tokens,
            output_tokens=output_tokens,
            cache_creation_tokens=cache_creation_tokens,
            cache_read_tokens=cache_read_tokens,
        )
