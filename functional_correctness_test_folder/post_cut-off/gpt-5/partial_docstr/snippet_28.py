from typing import Any, Dict, Optional


class PricingCalculator:
    MODEL_PRICING: Dict[str, Dict[str, float]] = {}

    def __init__(self, custom_pricing: Optional[Dict[str, Dict[str, float]]] = None) -> None:
        self.pricing: Dict[str, Dict[str, float]] = {}
        # Normalize and load default pricing
        for model, prices in self.MODEL_PRICING.items():
            self.pricing[model] = self._normalize_prices(prices)
        # Merge custom pricing (overrides defaults)
        if custom_pricing:
            for model, prices in custom_pricing.items():
                base = self.pricing.get(
                    model, {"input": 0.0, "output": 0.0, "cache_creation": 0.0, "cache_read": 0.0})
                base.update(self._normalize_prices(prices))
                self.pricing[model] = base

    def calculate_cost(self, model: str, input_tokens: int = 0, output_tokens: int = 0, cache_creation_tokens: int = 0, cache_read_tokens: int = 0, tokens: Optional[Any] = None, strict: bool = False) -> float:
        if tokens is not None:
            # Duck typing for TokenCounts-like objects or dicts
            if isinstance(tokens, dict):
                input_tokens = int(tokens.get(
                    "input_tokens", tokens.get("prompt_tokens", 0)) or 0)
                output_tokens = int(tokens.get(
                    "output_tokens", tokens.get("completion_tokens", 0)) or 0)
                cache_creation_tokens = int(tokens.get(
                    "cache_creation_tokens", tokens.get("cache_write_tokens", 0)) or 0)
                cache_read_tokens = int(
                    tokens.get("cache_read_tokens", 0) or 0)
            else:
                input_tokens = int(
                    getattr(tokens, "input_tokens", getattr(tokens, "prompt_tokens", 0)) or 0)
                output_tokens = int(getattr(tokens, "output_tokens", getattr(
                    tokens, "completion_tokens", 0)) or 0)
                cache_creation_tokens = int(getattr(
                    tokens, "cache_creation_tokens", getattr(tokens, "cache_write_tokens", 0)) or 0)
                cache_read_tokens = int(
                    getattr(tokens, "cache_read_tokens", 0) or 0)

        # Clamp negatives to zero
        input_tokens = max(0, int(input_tokens or 0))
        output_tokens = max(0, int(output_tokens or 0))
        cache_creation_tokens = max(0, int(cache_creation_tokens or 0))
        cache_read_tokens = max(0, int(cache_read_tokens or 0))

        pricing = self._get_pricing_for_model(model, strict=strict)

        per_million = 1_000_000.0
        cost = 0.0
        cost += (input_tokens / per_million) * pricing.get("input", 0.0)
        cost += (output_tokens / per_million) * pricing.get("output", 0.0)
        cost += (cache_creation_tokens / per_million) * \
            pricing.get("cache_creation", 0.0)
        cost += (cache_read_tokens / per_million) * \
            pricing.get("cache_read", 0.0)
        return float(cost)

    def _get_pricing_for_model(self, model: str, strict: bool = False) -> Dict[str, float]:
        # Exact match
        if model in self.pricing:
            return self.pricing[model]

        # Try prefix matches (e.g., versions like "-2024-xx-xx")
        candidates = [name for name in self.pricing.keys()
                      if model.startswith(name)]
        if candidates:
            # Longest prefix wins
            selected = max(candidates, key=len)
            return self.pricing[selected]

        # Try removing version suffixes separated by ":" or "@"
        for sep in (":", "@"):
            if sep in model:
                base = model.split(sep, 1)[0]
                if base in self.pricing:
                    return self.pricing[base]

        # Try progressively trimming dashed suffix segments
        if "-" in model:
            parts = model.split("-")
            for i in range(len(parts) - 1, 0, -1):
                base = "-".join(parts[:i])
                if base in self.pricing:
                    return self.pricing[base]

        if strict:
            raise KeyError(f"Unknown model for pricing: {model}")

        # Fallback to zero-cost pricing
        return {"input": 0.0, "output": 0.0, "cache_creation": 0.0, "cache_read": 0.0}

    def calculate_cost_for_entry(self, entry_data: Dict[str, Any], mode: Any) -> float:
        # Extract model
        model = (
            entry_data.get("model")
            or entry_data.get("response", {}).get("model")
            or entry_data.get("metadata", {}).get("model")
            or ""
        )

        # Extract tokens from various possible shapes
        tokens_obj = entry_data.get("tokens")
        usage = entry_data.get("usage") or {}

        input_tokens = entry_data.get("input_tokens")
        output_tokens = entry_data.get("output_tokens")
        cache_creation_tokens = entry_data.get(
            "cache_creation_tokens", entry_data.get("cache_write_tokens"))
        cache_read_tokens = entry_data.get("cache_read_tokens")

        # Fallbacks from usage dict
        if input_tokens is None:
            input_tokens = usage.get(
                "input_tokens", usage.get("prompt_tokens"))
        if output_tokens is None:
            output_tokens = usage.get(
                "output_tokens", usage.get("completion_tokens"))
        if cache_creation_tokens is None:
            cache_creation_tokens = usage.get(
                "cache_creation_tokens", usage.get("cache_write_tokens"))
        if cache_read_tokens is None:
            cache_read_tokens = usage.get("cache_read_tokens")

        # If tokens provided as a nested dict/object, prefer that API
        if tokens_obj is not None:
            return self.calculate_cost(
                model=model or "",
                tokens=tokens_obj,
            )

        return self.calculate_cost(
            model=model or "",
            input_tokens=int(input_tokens or 0),
            output_tokens=int(output_tokens or 0),
            cache_creation_tokens=int(cache_creation_tokens or 0),
            cache_read_tokens=int(cache_read_tokens or 0),
        )

    def _normalize_prices(self, prices: Dict[str, float]) -> Dict[str, float]:
        # Accept a variety of common keys and normalize to canonical keys
        key_map = {
            "input": "input",
            "input_per_million": "input",
            "input_usd_per_million": "input",
            "prompt": "input",
            "prompt_per_million": "input",
            "prompt_usd_per_million": "input",

            "output": "output",
            "output_per_million": "output",
            "output_usd_per_million": "output",
            "completion": "output",
            "completion_per_million": "output",
            "completion_usd_per_million": "output",

            "cache_creation": "cache_creation",
            "cache_creation_per_million": "cache_creation",
            "cache_creation_usd_per_million": "cache_creation",
            "cache_write": "cache_creation",
            "cache_write_per_million": "cache_creation",
            "cache_write_usd_per_million": "cache_creation",

            "cache_read": "cache_read",
            "cache_read_per_million": "cache_read",
            "cache_read_usd_per_million": "cache_read",
        }
        normalized = {"input": 0.0, "output": 0.0,
                      "cache_creation": 0.0, "cache_read": 0.0}
        for k, v in prices.items():
            if k in key_map:
                normalized[key_map[k]] = float(v)
        # Also accept already-normalized keys
        for k in ("input", "output", "cache_creation", "cache_read"):
            if k in prices:
                normalized[k] = float(prices[k])
        return normalized
