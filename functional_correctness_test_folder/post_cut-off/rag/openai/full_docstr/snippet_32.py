
from __future__ import annotations

import datetime
from typing import Any, Dict, Optional

# The following imports are assumed to exist in the surrounding codebase.
# They are referenced only for type checking and may be replaced with the
# actual implementations in the real project.
try:
    from .pricing import PricingCalculator
    from .timezone import TimezoneHandler
    from .usage import UsageEntry, CostMode
except Exception:  # pragma: no cover
    # Fallback stubs for type checking / documentation purposes.
    class PricingCalculator:
        def calculate_cost(self, tokens: Dict[str, int], mode: Any) -> float:
            return 0.0

    class TimezoneHandler:
        def convert(self, ts: datetime.datetime) -> datetime.datetime:
            return ts

    class UsageEntry:
        def __init__(
            self,
            *,
            timestamp: Optional[datetime.datetime] = None,
            model: str = "",
            tokens: Optional[Dict[str, int]] = None,
            metadata: Optional[Dict[str, str]] = None,
            cost: float = 0.0,
        ) -> None:
            self.timestamp = timestamp
            self.model = model
            self.tokens = tokens or {}
            self.metadata = metadata or {}
            self.cost = cost

    class CostMode:
        pass


class UsageEntryMapper:
    """Compatibility wrapper for legacy UsageEntryMapper interface.

    This class provides backward compatibility for tests that expect
    the old UsageEntryMapper interface, wrapping the new functional
    approach in `_map_to_usage_entry`.
    """

    def __init__(self, pricing_calculator: PricingCalculator, timezone_handler: TimezoneHandler):
        """Initialize with required components."""
        self.pricing_calculator = pricing_calculator
        self.timezone_handler = timezone_handler

    def map(self, data: Dict[str, Any], mode: CostMode) -> Optional[UsageEntry]:
        """Map raw data to UsageEntry - compatibility interface."""
        # Extract tokens; if missing or invalid, return None.
        tokens = data.get("tokens")
        if not isinstance(tokens, dict) or not self._has_valid_tokens(tokens):
            return None

        # Extract other fields.
        timestamp = self._extract_timestamp(data)
        if timestamp is not None:
            timestamp = self.timezone_handler.convert(timestamp)

        model = self._extract_model(data)
        metadata = self._extract_metadata(data)

        # Compute cost using the pricing calculator.
        cost = self.pricing_calculator.calculate_cost(tokens, mode)

        # Build and return the UsageEntry.
        return UsageEntry(
            timestamp=timestamp,
            model=model,
            tokens=tokens,
            metadata=metadata,
            cost=cost,
        )

    def _has_valid_tokens(self, tokens: Dict[str, int]) -> bool:
        """Check if tokens are valid (for test compatibility)."""
        # Tokens are considered valid if all values are non‑negative integers.
        return all(
            isinstance(v, int) and v >= 0
            for v in tokens.values()
        )

    def _extract_timestamp(self, data: Dict[str, Any]) -> Optional[datetime.datetime]:
        """Extract timestamp (for test compatibility)."""
        ts = data.get("timestamp")
        if ts is None:
            return None
        if isinstance(ts, datetime.datetime):
            return ts
        if isinstance(ts, str):
            try:
                # Try ISO‑8601 parsing first.
                return datetime.datetime.fromisoformat(ts)
            except ValueError:
                # Fallback: try parsing with common formats.
                for fmt in ("%Y-%m-%d %H:%M:%S", "%Y-%m-%dT%H:%M:%S"):
                    try:
                        return datetime.datetime.strptime(ts, fmt)
                    except ValueError:
                        continue
        return None

    def _extract_model(self, data: Dict[str, Any]) -> str:
        """Extract model name (for test compatibility)."""
        return str(data.get("model", ""))

    def _extract_metadata(self, data: Dict[str, Any]) -> Dict[str, str]:
        """Extract metadata (for test compatibility)."""
        meta = data.get("metadata", {})
        if isinstance(meta, dict):
            # Ensure all keys/values are strings.
            return {str(k): str(v) for k, v in meta.items()}
        return {}
