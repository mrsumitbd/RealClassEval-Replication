from typing import Optional, Dict, Any


class PricingCalculator:

    def __init__(self, custom_pricing: Optional[Dict[str, Dict[str, float]]] = None) -> None:
        self._pricing: Dict[str, Dict[str, float]] = {}
        if custom_pricing:
            for model, pricing in custom_pricing.items():
                self._pricing[model] = {
                    "input": float(pricing.get("input", pricing.get("input_token", 0.0))),
                    "output": float(pricing.get("output", pricing.get("output_token", 0.0))),
                    "cache_creation": float(pricing.get("cache_creation", pricing.get("cache_creation_token", 0.0))),
                    "cache_read": float(pricing.get("cache_read", pricing.get("cache_read_token", 0.0))),
                }

    def calculate_cost(
        self,
        model: str,
        input_tokens: int = 0,
        output_tokens: int = 0,
        cache_creation_tokens: int = 0,
        cache_read_tokens: int = 0,
        tokens: Optional[Any] = None,
        strict: bool = False
    ) -> float:
        if tokens is not None:
            input_tokens = self._get_token_count(
                tokens, "input_tokens", input_tokens)
            output_tokens = self._get_token_count(
                tokens, "output_tokens", output_tokens)
            cache_creation_tokens = self._get_token_count(
                tokens, "cache_creation_tokens", cache_creation_tokens)
            cache_read_tokens = self._get_token_count(
                tokens, "cache_read_tokens", cache_read_tokens)

        self._validate_non_negative(input_tokens, "input_tokens")
        self._validate_non_negative(output_tokens, "output_tokens")
        self._validate_non_negative(
            cache_creation_tokens, "cache_creation_tokens")
        self._validate_non_negative(cache_read_tokens, "cache_read_tokens")

        pricing = self._get_pricing_for_model(model, strict=strict)
        return (
            input_tokens * pricing.get("input", 0.0) +
            output_tokens * pricing.get("output", 0.0) +
            cache_creation_tokens * pricing.get("cache_creation", 0.0) +
            cache_read_tokens * pricing.get("cache_read", 0.0)
        )

    def _get_pricing_for_model(self, model: str, strict: bool = False) -> Dict[str, float]:
        if model in self._pricing:
            return self._pricing[model]
        if strict:
            raise ValueError(f"No pricing found for model '{model}'.")
        return {"input": 0.0, "output": 0.0, "cache_creation": 0.0, "cache_read": 0.0}

    def calculate_cost_for_entry(self, entry_data: Dict[str, Any], mode: Any) -> float:
        model = entry_data.get("model") or entry_data.get("model_name") or ""
        if not model:
            raise ValueError(
                "Model name is required in entry_data under 'model' or 'model_name'.")

        name = self._mode_name(mode)

        tokens_obj = entry_data.get("tokens") or entry_data.get("token_counts")
        input_tokens = entry_data.get("input_tokens", 0)
        output_tokens = entry_data.get("output_tokens", 0)
        cache_creation_tokens = entry_data.get("cache_creation_tokens", 0)
        cache_read_tokens = entry_data.get("cache_read_tokens", 0)

        if tokens_obj is not None:
            input_tokens = self._get_token_count(
                tokens_obj, "input_tokens", input_tokens)
            output_tokens = self._get_token_count(
                tokens_obj, "output_tokens", output_tokens)
            cache_creation_tokens = self._get_token_count(
                tokens_obj, "cache_creation_tokens", cache_creation_tokens)
            cache_read_tokens = self._get_token_count(
                tokens_obj, "cache_read_tokens", cache_read_tokens)

        if name in ("total", "all"):
            pass
        elif name in ("input", "prompt"):
            output_tokens = 0
            cache_creation_tokens = 0
            cache_read_tokens = 0
        elif name in ("output", "completion"):
            input_tokens = 0
            cache_creation_tokens = 0
            cache_read_tokens = 0
        elif name in ("cache_creation", "cache-create", "cachecreate"):
            input_tokens = 0
            output_tokens = 0
            cache_read_tokens = 0
        elif name in ("cache_read", "cache-read", "cacheread"):
            input_tokens = 0
            output_tokens = 0
            cache_creation_tokens = 0
        elif name in ("cache", "caching"):
            input_tokens = 0
            output_tokens = 0
        else:
            raise ValueError(f"Unsupported cost mode: {mode}")

        return self.calculate_cost(
            model=model,
            input_tokens=int(input_tokens or 0),
            output_tokens=int(output_tokens or 0),
            cache_creation_tokens=int(cache_creation_tokens or 0),
            cache_read_tokens=int(cache_read_tokens or 0),
            strict=False
        )

    @staticmethod
    def _get_token_count(source: Any, attr: str, default: int = 0) -> int:
        if source is None:
            return int(default)
        if isinstance(source, dict):
            return int(source.get(attr, default) or 0)
        if hasattr(source, attr):
            return int(getattr(source, attr) or 0)
        return int(default)

    @staticmethod
    def _mode_name(mode: Any) -> str:
        if mode is None:
            return "total"
        if isinstance(mode, str):
            return mode.strip().lower()
        name = getattr(mode, "name", None)
        if name:
            return str(name).strip().lower()
        value = getattr(mode, "value", None)
        if isinstance(value, str):
            return value.strip().lower()
        return "total"

    @staticmethod
    def _validate_non_negative(value: int, name: str) -> None:
        if value is None:
            return
        if value < 0:
            raise ValueError(f"{name} cannot be negative: {value}")
