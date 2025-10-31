from typing import Optional, Dict, Any, Tuple
from dataclasses import dataclass
from enum import Enum, auto
import copy


@dataclass(frozen=True)
class TokenCounts:
    input_tokens: int = 0
    output_tokens: int = 0
    cache_creation_tokens: int = 0
    cache_read_tokens: int = 0


class CostMode(Enum):
    TOTAL = auto()
    INPUT_ONLY = auto()
    OUTPUT_ONLY = auto()
    CACHE_ONLY = auto()


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

    # Fallback hardcoded pricing (USD per 1K tokens)
    DEFAULT_MODEL_PRICING: Dict[str, Dict[str, float]] = {
        # OpenAI family (approximate defaults, can be overridden)
        "gpt-4o": {
            "input": 0.005,
            "output": 0.015,
            "cache_creation": 0.010,
            "cache_read": 0.001,
        },
        "gpt-4o-mini": {
            "input": 0.0005,
            "output": 0.0015,
            "cache_creation": 0.0005,
            "cache_read": 0.0001,
        },
        "gpt-4.1": {
            "input": 0.005,
            "output": 0.015,
            "cache_creation": 0.010,
            "cache_read": 0.001,
        },
        "gpt-4.1-mini": {
            "input": 0.0005,
            "output": 0.0015,
            "cache_creation": 0.0005,
            "cache_read": 0.0001,
        },
        "gpt-3.5-turbo": {
            "input": 0.0005,
            "output": 0.0015,
            "cache_creation": 0.0005,
            "cache_read": 0.0001,
        },
        # Reasoning-oriented placeholders
        "o3": {
            "input": 0.010,
            "output": 0.030,
            "cache_creation": 0.012,
            "cache_read": 0.001,
        },
        "o3-mini": {
            "input": 0.0015,
            "output": 0.003,
            "cache_creation": 0.0015,
            "cache_read": 0.0002,
        },
    }

    def __init__(self, custom_pricing: Optional[Dict[str, Dict[str, float]]] = None) -> None:
        '''Initialize with optional custom pricing.
        Args:
            custom_pricing: Optional custom pricing dictionary to override defaults.
                          Should follow same structure as MODEL_PRICING.
        '''
        base = copy.deepcopy(self.DEFAULT_MODEL_PRICING)
        if custom_pricing:
            for model, pricing in custom_pricing.items():
                if model not in base:
                    base[model] = {}
                base[model].update(pricing or {})
        self._pricing: Dict[str, Dict[str, float]] = base
        self._cost_cache: Dict[Tuple[str, int, int, int, int], float] = {}

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
        if tokens is not None:
            input_tokens = getattr(tokens, "input_tokens", 0) or 0
            output_tokens = getattr(tokens, "output_tokens", 0) or 0
            cache_creation_tokens = getattr(
                tokens, "cache_creation_tokens", 0) or 0
            cache_read_tokens = getattr(tokens, "cache_read_tokens", 0) or 0

        key = (model, int(input_tokens), int(output_tokens),
               int(cache_creation_tokens), int(cache_read_tokens))
        if key in self._cost_cache:
            return self._cost_cache[key]

        pricing = self._get_pricing_for_model(model, strict=strict)

        # Normalize missing pricing keys to 0
        in_rate = float(pricing.get("input", 0.0))
        out_rate = float(pricing.get("output", 0.0))
        create_rate = float(pricing.get("cache_creation", 0.0))
        read_rate = float(pricing.get("cache_read", 0.0))

        cost = (
            (input_tokens / 1000.0) * in_rate
            + (output_tokens / 1000.0) * out_rate
            + (cache_creation_tokens / 1000.0) * create_rate
            + (cache_read_tokens / 1000.0) * read_rate
        )

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
        # 1. Exact match
        if model in self._pricing:
            return self._pricing[model]

        # 2. Common normalization attempts
        candidates = []
        for sep in ("@", ":", "/"):
            if sep in model:
                candidates.append(model.split(sep)[0])
        candidates.append(model)

        # 3. Progressive dash truncation (e.g., gpt-4o-2024-08-06 -> gpt-4o)
        parts = model.split("-")
        for i in range(len(parts), 1, -1):
            candidates.append("-".join(parts[:i]))
        if parts:
            candidates.append(parts[0])

        # 4. Longest-prefix match: prefer pricing keys that are prefixes of candidate or vice versa
        best_key = None
        best_len = -1
        keys = list(self._pricing.keys())
        for cand in candidates:
            for k in keys:
                if cand == k:
                    return self._pricing[k]
                if cand.startswith(k):
                    if len(k) > best_len:
                        best_key = k
                        best_len = len(k)
                elif k.startswith(cand):
                    if len(cand) > best_len:
                        best_key = k
                        best_len = len(cand)

        if best_key:
            return self._pricing[best_key]

        if strict:
            raise KeyError(f"Unknown model for pricing: {model}")

        # Fallback to zero-cost pricing if unknown and not strict
        return {"input": 0.0, "output": 0.0, "cache_creation": 0.0, "cache_read": 0.0}

    def calculate_cost_for_entry(self, entry_data: Dict[str, Any], mode: CostMode) -> float:
        '''Calculate cost for a single entry (backward compatibility).
        Args:
            entry_data: Entry data dictionary
            mode: Cost mode (for backward compatibility)
        Returns:
            Cost in USD
        '''
        model = entry_data.get("model") or entry_data.get("model_name") or ""

        # Gather tokens from possible shapes
        if "tokens" in entry_data and isinstance(entry_data["tokens"], dict):
            tdict = entry_data["tokens"]
            t = TokenCounts(
                input_tokens=int(tdict.get("input_tokens", 0) or 0),
                output_tokens=int(tdict.get("output_tokens", 0) or 0),
                cache_creation_tokens=int(
                    tdict.get("cache_creation_tokens", 0) or 0),
                cache_read_tokens=int(tdict.get("cache_read_tokens", 0) or 0),
            )
        else:
            t = TokenCounts(
                input_tokens=int(entry_data.get("input_tokens", 0) or 0),
                output_tokens=int(entry_data.get("output_tokens", 0) or 0),
                cache_creation_tokens=int(entry_data.get(
                    "cache_creation_tokens", 0) or 0),
                cache_read_tokens=int(entry_data.get(
                    "cache_read_tokens", 0) or 0),
            )

        pricing = self._get_pricing_for_model(model, strict=False)
        in_rate = float(pricing.get("input", 0.0))
        out_rate = float(pricing.get("output", 0.0))
        create_rate = float(pricing.get("cache_creation", 0.0))
        read_rate = float(pricing.get("cache_read", 0.0))

        input_cost = (t.input_tokens / 1000.0) * in_rate
        output_cost = (t.output_tokens / 1000.0) * out_rate
        cache_create_cost = (t.cache_creation_tokens / 1000.0) * create_rate
        cache_read_cost = (t.cache_read_tokens / 1000.0) * read_rate

        if mode == CostMode.INPUT_ONLY:
            return input_cost
        if mode == CostMode.OUTPUT_ONLY:
            return output_cost
        if mode == CostMode.CACHE_ONLY:
            return cache_create_cost + cache_read_cost
        # Default: total
        return input_cost + output_cost + cache_create_cost + cache_read_cost
