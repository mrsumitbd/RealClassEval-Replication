
from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import Any, Dict, Optional

# Placeholder imports – in real code these would come from the actual modules
# from pricing import PricingCalculator
# from timezone import TimezoneHandler
# from cost import CostMode
# from usage import UsageEntry

# Minimal stubs for the missing types (replace with real imports in production)


class PricingCalculator:
    def calculate_cost(self, tokens: Dict[str, int], model: str, timestamp: datetime) -> float:
        # Dummy implementation – replace with real pricing logic
        return (tokens.get("input", 0) + tokens.get("output", 0)) * 0.0001


class TimezoneHandler:
    def to_utc(self, dt: datetime) -> datetime:
        # Dummy implementation – replace with real timezone conversion
        return dt


class CostMode:
    pass


@dataclass
class UsageEntry:
    timestamp: datetime
    model: str
    metadata: Dict[str, str]
    tokens: Dict[str, int]
    cost: float
    mode: CostMode


class UsageEntryMapper:
    def __init__(self, pricing_calculator: PricingCalculator, timezone_handler: TimezoneHandler):
        self.pricing_calculator = pricing_calculator
        self.timezone_handler = timezone_handler

    def map(self, data: Dict[str, Any], mode: CostMode) -> Optional[UsageEntry]:
        """
        Convert raw data into a UsageEntry if all required fields are present and valid.
        """
        # Extract and validate timestamp
        timestamp = self._extract_timestamp(data)
        if timestamp is None:
            return None

        # Extract model name
        model = self._extract_model(data)

        # Extract metadata
        metadata = self._extract_metadata(data)

        # Extract tokens and validate
        tokens = data.get("tokens", {})
        if not self._has_valid_tokens(tokens):
            return None

        # Calculate cost
        cost = self.pricing_calculator.calculate_cost(tokens, model, timestamp)

        return UsageEntry(
            timestamp=timestamp,
            model=model,
            metadata=metadata,
            tokens=tokens,
            cost=cost,
            mode=mode,
        )

    def _has_valid_tokens(self, tokens: Dict[str, int]) -> bool:
        """
        Ensure that the tokens dictionary contains integer values for both
        'input' and 'output' keys and that they are non-negative.
        """
        if not isinstance(tokens, dict):
            return False
        required_keys = {"input", "output"}
        if not required_keys.issubset(tokens.keys()):
            return False
        for key in required_keys:
            value = tokens.get(key)
            if not isinstance(value, int) or value < 0:
                return False
        return True

    def _extract_timestamp(self, data: Dict[str, Any]) -> Optional[datetime]:
        """
        Extract a datetime object from the data dictionary. Supports ISO 8601 strings
        and Unix epoch timestamps (int/float). Returns None if extraction fails.
        """
        ts = data.get("timestamp")
        if ts is None:
            return None

        # If it's already a datetime instance
        if isinstance(ts, datetime):
            return self.timezone_handler.to_utc(ts)

        # Try ISO 8601 string
        if isinstance(ts, str):
            try:
                dt = datetime.fromisoformat(ts)
                return self.timezone_handler.to_utc(dt)
            except ValueError:
                pass

        # Try numeric epoch
        if isinstance(ts, (int, float)):
            try:
                dt = datetime.fromtimestamp(ts)
                return self.timezone_handler.to_utc(dt)
            except (OSError, OverflowError):
                pass

        return None

    def _extract_model(self, data: Dict[str, Any]) -> str:
        """
        Return the model name from the data dictionary, defaulting to 'unknown'.
        """
        return str(data.get("model", "unknown"))

    def _extract_metadata(self, data: Dict[str, Any]) -> Dict[str, str]:
        """
        Return a dictionary of string key/value pairs from the 'metadata' field.
        Non-string values are converted to strings. Missing metadata defaults to an empty dict.
        """
        raw_meta = data.get("metadata", {})
        if not isinstance(raw_meta, dict):
            return {}
        return {str(k): str(v) for k, v in raw_meta.items()}
