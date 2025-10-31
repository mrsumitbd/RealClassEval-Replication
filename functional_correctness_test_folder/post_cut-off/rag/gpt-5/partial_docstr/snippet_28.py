from __future__ import annotations

from typing import Optional, Dict, Any, Mapping, Tuple, Union
from dataclasses import dataclass
from enum import Enum
import threading


# Fallback pricing (per 1k tokens)
_DEFAULT_MODEL_PRICING: Dict[str, Dict[str, float]] = {
    "default": {
        "input_per_1k": 0.005,
        "output_per_1k": 0.015,
        "cache_creation_per_1k": 0.0,
        "cache_read_per_1k": 0.0,
    },
    "gpt-4o": {
        "input_per_1k": 0.005,
        "output_per_1k": 0.015,
        "cache_creation_per_1k": 0.0,
        "cache_read_per_1k": 0.0,
    },
    "gpt-4o-mini": {
        "input_per_1k": 0.00015,
        "output_per_1k": 0.0006,
        "cache_creation_per_1k": 0.0,
        "cache_read_per_1k": 0.0,
    },
}


# Fallback TokenCounts type (for compatibility)
@dataclass
class _TokenCountsFallback:
    input_tokens: int = 0
    output_tokens: int = 0
    cache_creation_tokens: int = 0
    cache_read_tokens: int = 0
    # common aliases
    prompt_tokens: int = 0
    completion_tokens: int = 0


try:
    # If a TokenCounts type exists elsewhere, we will just use the annotation
    TokenCounts = _TokenCountsFallback  # type: ignore[assignment]
except Exception:
    TokenCounts = _TokenCountsFallback  # type: ignore[assignment]


# Fallback CostMode enum (for compatibility, not used in logic)
class CostMode(Enum):
    TOTAL = "total"
    DETAILED = "detailed"


def _to_int(value: Any) -> int:
    try:
        if value is None:
            return 0
        if isinstance(value, bool):
            return int(value)
        if isinstance(value, (int,)):
            return max(0, int(value))
        if isinstance(value, float):
            return max(0, int(round(value)))
        if isinstance(value, str) and value.strip().isdigit():
            return max(0, int(value.strip()))
    except Exception:
        pass
    return 0


def _normalize_model_name(model: str) -> str:
    name = (model or "").strip()
    name = name.replace("\n", " ").strip()
    name = name.split("/")[-1] if "/" in name else name
    name = name.split(":")[0] if ":" in name else name
    return name.lower()


def _normalize_pricing(pr: Mapping[str, float]) -> Dict[str, float]:
    # Accept a variety of key names and normalize to per_1k keys
    out: Dict[str, float] = {
        "input_per_1k": 0.0,
        "output_per_1k": 0.0,
        "cache_creation_per_1k": 0.0,
        "cache_read_per_1k": 0.0,
    }

    def pick(keys: Tuple[str, ...]) -> Optional[float]:
        for k in keys:
            if k in pr:
                return float(pr[k])
        return None

    # Support both per token and per 1k token pricing; per-token keys end with _per_token
    in_ = pick(("input_per_1k", "prompt_per_1k", "in_per_1k"))
    out_ = pick(("output_per_1k", "completion_per_1k", "out_per_1k"))
    cc_ = pick(("cache_creation_per_1k", "cache_write_per_1k"))
    cr_ = pick(("cache_read_per_1k",))

    in_tok = pick(("input_per_token", "prompt_per_token", "in_per_token"))
    out_tok = pick(
        ("output_per_token", "completion_per_token", "out_per_token"))
    cc_tok = pick(("cache_creation_per_token", "cache_write_per_token"))
    cr_tok = pick(("cache_read_per_token",))

    if in_ is None and in_tok is not None:
        in_ = in_tok * 1000.0
    if out_ is None and out_tok is not None:
        out_ = out_tok * 1000.0
    if cc_ is None and cc_tok is not None:
        cc_ = cc_tok * 1000.0
    if cr_ is None and cr_tok is not None:
        cr_ = cr_tok * 1000.0

    if in_ is not None:
        out["input_per_1k"] = in_
    if out_ is not None:
        out["output_per_1k"] = out_
    if cc_ is not None:
        out["cache_creation_per_1k"] = cc_
    if cr_ is not None:
        out["cache_read_per_1k"] = cr_

    return out


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
        base = dict(_DEFAULT_MODEL_PRICING)
        if custom_pricing:
            for k, v in custom_pricing.items():
                base[_normalize_model_name(k)] = _normalize_pricing(v)
        # Normalize all pricing entries
        self._pricing: Dict[str, Dict[str, float]] = {
            _normalize_model_name(k): _normalize_pricing(v) for k, v in base.items()
        }
        # Ensure default exists
        if "default" not in self._pricing:
            self._pricing["default"] = _normalize_pricing(
                _DEFAULT_MODEL_PRICING["default"])

        self._cache_lock = threading.Lock()
        self._cost_cache: Dict[Tuple[str, int, int, int,
                                     int, float, float, float, float], float] = {}
        self._pricing_version = 1

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
        # Extract counts
        if tokens is not None:
            inp, outp, ccreate, cread = self._extract_from_tokens(tokens)
        else:
            inp = _to_int(input_tokens)
            outp = _to_int(output_tokens)
            ccreate = _to_int(cache_creation_tokens)
            cread = _to_int(cache_read_tokens)

        pr = self._get_pricing_for_model(model, strict=strict)
        rin = float(pr.get("input_per_1k", 0.0))
        rout = float(pr.get("output_per_1k", 0.0))
        rcc = float(pr.get("cache_creation_per_1k", 0.0))
        rcr = float(pr.get("cache_read_per_1k", 0.0))

        key = (_normalize_model_name(model), inp, outp,
               ccreate, cread, rin, rout, rcc, rcr)
        with self._cache_lock:
            cached = self._cost_cache.get(key)
            if cached is not None:
                return cached

        cost = (inp * rin + outp * rout + ccreate * rcc + cread * rcr) / 1000.0

        with self._cache_lock:
            self._cost_cache[key] = cost

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
        name = _normalize_model_name(model)
        pr = self._pricing.get(name)
        if pr is not None:
            return pr

        # Try to match by longest prefix among known models
        candidates = [(k, v) for k, v in self._pricing.items()
                      if k != "default" and name.startswith(k)]
        if candidates:
            candidates.sort(key=lambda kv: len(kv[0]), reverse=True)
            return candidates[0][1]

        if strict:
            raise KeyError(f"Unknown model pricing for '{model}'")

        return self._pricing["default"]

    def calculate_cost_for_entry(self, entry_data: Dict[str, Any], mode: CostMode) -> float:
        '''Calculate cost for a single entry (backward compatibility).
        Args:
            entry_data: Entry data dictionary
            mode: Cost mode (for backward compatibility)
        Returns:
            Cost in USD
        '''
        model = entry_data.get("model") or entry_data.get(
            "name") or entry_data.get("model_name") or "default"

        # Usage may be nested under 'usage' or at top level
        usage = entry_data.get("usage") if isinstance(
            entry_data.get("usage"), Mapping) else {}

        # Try to extract tokens from a nested 'tokens' field if present
        tokens_field = entry_data.get("tokens") or usage.get("tokens")

        if tokens_field is not None:
            return self.calculate_cost(model=model, tokens=tokens_field, strict=False)

        # Otherwise pull fields individually with broad alias support
        inp = self._pick_first(
            entry_data, usage, "input_tokens", "prompt_tokens", "tokens_in", "in_tokens")
        outp = self._pick_first(entry_data, usage, "output_tokens",
                                "completion_tokens", "tokens_out", "out_tokens")
        ccreate = self._pick_first(
            entry_data, usage,
            "cache_creation_tokens", "cache_creation_input_tokens", "cache_write_tokens"
        )
        cread = self._pick_first(
            entry_data, usage,
            "cache_read_tokens", "cache_read_input_tokens"
        )

        return self.calculate_cost(
            model=model,
            input_tokens=_to_int(inp),
            output_tokens=_to_int(outp),
            cache_creation_tokens=_to_int(ccreate),
            cache_read_tokens=_to_int(cread),
            strict=False,
        )

    def _extract_from_tokens(self, tokens: Union[TokenCounts, Mapping[str, Any]]) -> Tuple[int, int, int, int]:
        # Support dataclass/obj with attributes and plain mappings
        if isinstance(tokens, Mapping):
            get = lambda *keys: next((tokens[k]
                                     for k in keys if k in tokens), 0)
        else:
            get = lambda *keys: next((getattr(tokens, k)
                                     for k in keys if hasattr(tokens, k)), 0)

        inp = _to_int(get("input_tokens", "prompt_tokens", "in_tokens"))
        outp = _to_int(get("output_tokens", "completion_tokens", "out_tokens"))
        ccreate = _to_int(get("cache_creation_tokens",
                          "cache_creation_input_tokens", "cache_write_tokens"))
        cread = _to_int(get("cache_read_tokens", "cache_read_input_tokens"))
        return inp, outp, ccreate, cread

    @staticmethod
    def _pick_first(primary: Mapping[str, Any], secondary: Mapping[str, Any], *keys: str) -> Any:
        for k in keys:
            if k in primary:
                return primary[k]
            if k in secondary:
                return secondary[k]
        return 0
