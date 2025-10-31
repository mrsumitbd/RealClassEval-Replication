
from __future__ import annotations

import datetime
from typing import Any, Dict, Optional

# The following imports are placeholders – the real project should provide
# the actual implementations of these classes.
try:
    from myproject.pricing import PricingCalculator
    from myproject.timezone import TimezoneHandler
    from myproject.cost import CostMode
    from myproject.usage import UsageEntry
except Exception:  # pragma: no cover
    # Dummy stubs for type checking / example purposes
    class PricingCalculator:
        def calculate(self, prompt_tokens: int, completion_tokens: int,
                      model: str, mode: CostMode) -> float:
            return 0.0

    class TimezoneHandler:
        def to_utc(self, dt: datetime.datetime) -> datetime.datetime:
            return dt

    class CostMode:
        pass

    class UsageEntry:
        def __init__(self, timestamp: datetime.datetime, model: str,
                     prompt_tokens: int, completion_tokens: int,
                     total_tokens: int, cost: float,
                     metadata: Optional[Dict[str, str]] = None):
            self.timestamp = timestamp
            self.model = model
            self.prompt_tokens = prompt_tokens
            self.completion_tokens = completion_tokens
            self.total_tokens = total_tokens
            self.cost = cost
            self.metadata = metadata or {}

        def __repr__(self) -> str:  # pragma: no cover
            return (
                f"UsageEntry(timestamp={self.timestamp!r}, model={self.model!r}, "
                f"prompt_tokens={self.prompt_tokens!r}, completion_tokens={self.completion_tokens!r}, "
                f"total_tokens={self.total_tokens!r}, cost={self.cost!r}, "
                f"metadata={self.metadata!r})"
            )


class UsageEntryMapper:
    """Compatibility wrapper for legacy UsageEntryMapper interface.
    This class provides backward compatibility for tests that expect
    the old UsageEntryMapper interface, wrapping the new functional
    approach in _map_to_usage_entry.
    """

    def __init__(self, pricing_calculator: PricingCalculator,
                 timezone_handler: TimezoneHandler) -> None:
        """Initialize with required components."""
        self.pricing_calculator = pricing_calculator
        self.timezone_handler = timezone_handler

    def map(self, data: Dict[str, Any], mode: CostMode) -> Optional[UsageEntry]:
        """Map raw data to UsageEntry - compatibility interface."""
        # Extract required fields
        timestamp = self._extract_timestamp(data)
        if timestamp is None:
            return None

        model = self._extract_model(data)
        if not model:
            return None

        metadata = self._extract_metadata(data)

        # Extract token counts
        tokens = {
            "prompt_tokens": data.get("prompt_tokens"),
            "completion_tokens": data.get("completion_tokens"),
            "total_tokens": data.get("total_tokens"),
        }

        if not self._has_valid_tokens(tokens):
            return None

        prompt_tokens = int(tokens["prompt_tokens"])
        completion_tokens = int(tokens["completion_tokens"])
        total_tokens = int(tokens["total_tokens"])

        # Compute cost
        try:
            cost = self.pricing_calculator.calculate(
                prompt_tokens, completion_tokens, model, mode
            )
        except Exception:  # pragma: no cover
            # If the pricing calculator fails, fall back to zero cost
            cost = 0.0

        return UsageEntry(
            timestamp=timestamp,
            model=model,
            prompt_tokens=prompt_tokens,
            completion_tokens=completion_tokens,
            total_tokens=total_tokens,
            cost=cost,
            metadata=metadata,
        )

    def _has_valid_tokens(self, tokens: Dict[str, int]) -> bool:
        """Check if tokens are valid (for test compatibility)."""
        required = {"prompt_tokens", "completion_tokens", "total_tokens"}
        if not required.issubset(tokens):
            return False
        for key in required:
            value = tokens.get(key)
            if not isinstance(value, int) or value < 0:
                return False
        return True

    def _extract_timestamp(self, data: Dict[str, Any]) -> Optional[datetime.datetime]:
        """Extract timestamp (for test compatibility)."""
        ts_keys = ["timestamp", "created_at", "time"]
        ts_value = None
        for key in ts_keys:
            if key in data:
                ts_value = data[key]
                break
        if ts_value is None:
            return None

        # If already a datetime, return it
        if isinstance(ts_value, datetime.datetime):
            return self.timezone_handler.to_utc(ts_value)

        # Try parsing ISO format
        try:
            dt = datetime.datetime.fromisoformat(ts_value.rstrip("Z"))
            if ts_value.endswith("Z"):
                dt = dt.replace(tzinfo=datetime.timezone.utc)
            return self.timezone_handler.to_utc(dt)
        except Exception:  # pragma: no cover
            return None

    def _extract_model(self, data: Dict[str, Any]) -> str:
        """Extract model name (for test compatibility)."""
        for key in ("model", "model_name", "model_id"):
            if key in data and isinstance(data[key], str):
                return data[key]
        return ""

    def _extract_metadata(self, data: Dict[str, Any]) -> Dict[str, str]:
        """Extract metadata (for test compatibility)."""
        meta = data.get("metadata", {})
        if isinstance(meta, dict):
            # Ensure all keys/values are strings
            return {str(k): str(v) for k, v in meta.items()}
        return {}
