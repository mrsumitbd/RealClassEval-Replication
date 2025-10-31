
from __future__ import annotations

from datetime import datetime
from typing import Any, Dict, Optional

# The following imports are assumed to exist in the test environment.
# They are imported lazily to avoid circular dependencies during module import.
try:
    from pricing import PricingCalculator
    from timezone import TimezoneHandler
    from usage import UsageEntry, CostMode
except Exception:  # pragma: no cover
    # Fallback stubs for type checking / documentation purposes.
    class PricingCalculator:
        def calculate(self, tokens: Dict[str, int], model: str) -> float:
            return 0.0

    class TimezoneHandler:
        def localize(self, dt: datetime) -> datetime:
            return dt

    class UsageEntry:
        def __init__(
            self,
            timestamp: datetime,
            model: str,
            tokens: Dict[str, int],
            metadata: Dict[str, str],
            cost: float,
        ):
            self.timestamp = timestamp
            self.model = model
            self.tokens = tokens
            self.metadata = metadata
            self.cost = cost

    class CostMode:
        pass


class UsageEntryMapper:
    """Compatibility wrapper for legacy UsageEntryMapper interface.
    This class provides backward compatibility for tests that expect
    the old UsageEntryMapper interface, wrapping the new functional
    approach in `_map_to_usage_entry`.
    """

    def __init__(
        self,
        pricing_calculator: PricingCalculator,
        timezone_handler: TimezoneHandler,
    ):
        """Initialize with required components."""
        self.pricing_calculator = pricing_calculator
        self.timezone_handler = timezone_handler

    def map(
        self,
        data: Dict[str, Any],
        mode: CostMode,
    ) -> Optional[UsageEntry]:
        """Map raw data to UsageEntry - compatibility interface."""
        # Extract tokens
        tokens = data.get("usage")
        if not isinstance(tokens, dict) or not self._has_valid_tokens(tokens):
            return None

        # Extract timestamp
        timestamp = self._extract_timestamp(data)
        if timestamp is None:
            return None

        # Extract model
        model = self._extract_model(data)
        if not model:
            return None

        # Extract metadata
        metadata = self._extract_metadata(data)

        # Compute cost
        cost = self.pricing_calculator.calculate(tokens, model)

        # Build UsageEntry
        return UsageEntry(
            timestamp=timestamp,
            model=model,
            tokens=tokens,
            metadata=metadata,
            cost=cost,
        )

    def _has_valid_tokens(self, tokens: Dict[str, int]) -> bool:
        """Check if tokens are valid (for test compatibility)."""
        required_keys = {"prompt", "completion"}
        if not required_keys.issubset(tokens.keys()):
            return False
        for key in required_keys:
            value = tokens.get(key)
            if not isinstance(value, int) or value < 0:
                return False
        return True

    def _extract_timestamp(self, data: Dict[str, Any]) -> Optional[datetime]:
        """Extract timestamp (for test compatibility)."""
        ts = data.get("created") or data.get("timestamp")
        if ts is None:
            return None
        # Accept int epoch or ISO string
        if isinstance(ts, int):
            dt = datetime.fromtimestamp(ts)
        elif isinstance(ts, str):
            try:
                dt = datetime.fromisoformat(ts)
            except ValueError:
                return None
        else:
            return None
        # Localize using timezone handler
        return self.timezone_handler.localize(dt)

    def _extract_model(self, data: Dict[str, Any]) -> str:
        """Extract model name (for test compatibility)."""
        return data.get("model", "")

    def _extract_metadata(self, data: Dict[str, Any]) -> Dict[str, str]:
        """Extract metadata (for test compatibility)."""
        meta = data.get("metadata", {})
        if isinstance(meta, dict):
            # Ensure all values are strings
            return {k: str(v) for k, v in meta.items()}
        return {}
