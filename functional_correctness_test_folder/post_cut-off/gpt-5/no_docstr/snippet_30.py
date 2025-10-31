from dataclasses import dataclass, field
from typing import Dict, Any, Optional, Union

Number = Union[int, float]


def _as_int(value: Any, default: int = 0) -> int:
    try:
        if value is None:
            return default
        if isinstance(value, bool):
            return int(value)
        return int(value)
    except (ValueError, TypeError):
        return default


def _as_float(value: Any, default: float = 0.0) -> float:
    try:
        if value is None:
            return default
        if isinstance(value, bool):
            return float(int(value))
        return float(value)
    except (ValueError, TypeError):
        return default


@dataclass
class AggregatedStats:
    requests: int = 0
    input_tokens: int = 0
    output_tokens: int = 0
    cost: float = 0.0
    per_model: Dict[str, Dict[str, Number]] = field(default_factory=dict)

    def _extract_input_tokens(self, entry: "UsageEntry") -> int:
        candidates = (
            getattr(entry, "input_tokens", None),
            getattr(entry, "prompt_tokens", None),
            getattr(entry, "tokens_input", None),
            getattr(entry, "prompt", None),
        )
        for c in candidates:
            v = _as_int(c, None) if c is not None else None
            if v is not None:
                return max(0, v)
        # fallback from total if only total available
        total = getattr(entry, "total_tokens", None)
        if total is None:
            total = getattr(entry, "tokens", None)
        return max(0, _as_int(total, 0)) if total is not None else 0

    def _extract_output_tokens(self, entry: "UsageEntry") -> int:
        candidates = (
            getattr(entry, "output_tokens", None),
            getattr(entry, "completion_tokens", None),
            getattr(entry, "tokens_output", None),
            getattr(entry, "completion", None),
        )
        for c in candidates:
            v = _as_int(c, None) if c is not None else None
            if v is not None:
                return max(0, v)
        return 0

    def _extract_cost(self, entry: "UsageEntry") -> float:
        candidates = (
            getattr(entry, "cost", None),
            getattr(entry, "price", None),
            getattr(entry, "usd_cost", None),
            getattr(entry, "amount", None),
        )
        for c in candidates:
            v = _as_float(c, None) if c is not None else None
            if v is not None:
                return max(0.0, v)
        return 0.0

    def _extract_model(self, entry: "UsageEntry") -> str:
        model = getattr(entry, "model", None)
        if not model:
            model = getattr(entry, "model_name", None)
        if not model:
            model = "unknown"
        return str(model)

    def add_entry(self, entry: "UsageEntry") -> None:
        model = self._extract_model(entry)
        in_tok = self._extract_input_tokens(entry)
        out_tok = self._extract_output_tokens(entry)
        # If only total exists and we already used it for input, avoid double counting
        if out_tok == 0:
            # If entry provides an explicit total, ensure we don't exceed it
            total = getattr(entry, "total_tokens", None)
            if total is None:
                total = getattr(entry, "tokens", None)
            total_i = _as_int(total, None) if total is not None else None
            if total_i is not None and total_i >= in_tok:
                out_tok = max(0, total_i - in_tok)

        cst = self._extract_cost(entry)

        self.requests += 1
        self.input_tokens += in_tok
        self.output_tokens += out_tok
        self.cost += cst

        bucket = self.per_model.setdefault(
            model, {"requests": 0, "input_tokens": 0,
                    "output_tokens": 0, "total_tokens": 0, "cost": 0.0}
        )
        bucket["requests"] = int(bucket.get("requests", 0)) + 1
        bucket["input_tokens"] = int(bucket.get("input_tokens", 0)) + in_tok
        bucket["output_tokens"] = int(bucket.get("output_tokens", 0)) + out_tok
        bucket["total_tokens"] = int(bucket.get(
            "total_tokens", 0)) + (in_tok + out_tok)
        bucket["cost"] = float(bucket.get("cost", 0.0)) + cst

    def to_dict(self) -> Dict[str, Any]:
        total_tokens = self.input_tokens + self.output_tokens
        return {
            "requests": self.requests,
            "input_tokens": self.input_tokens,
            "output_tokens": self.output_tokens,
            "total_tokens": total_tokens,
            "cost": self.cost,
            "per_model": self.per_model,
        }
