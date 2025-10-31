
from typing import Dict, Any, Optional
from datetime import datetime
from enum import Enum


class CostMode(Enum):
    DETAILED = 1
    SUMMARY = 2


class PricingCalculator:
    def calculate_cost(self, usage_entry: 'UsageEntry') -> float:
        pass


class TimezoneHandler:
    def convert_to_utc(self, timestamp: datetime) -> datetime:
        pass


class UsageEntry:
    def __init__(self, timestamp: datetime, model: str, metadata: Dict[str, str], cost: float):
        self.timestamp = timestamp
        self.model = model
        self.metadata = metadata
        self.cost = cost


class UsageEntryMapper:
    '''Compatibility wrapper for legacy UsageEntryMapper interface.
    This class provides backward compatibility for tests that expect
    the old UsageEntryMapper interface, wrapping the new functional
    approach in _map_to_usage_entry.
    '''

    def __init__(self, pricing_calculator: PricingCalculator, timezone_handler: TimezoneHandler):
        '''Initialize with required components.'''
        self.pricing_calculator = pricing_calculator
        self.timezone_handler = timezone_handler

    def map(self, data: Dict[str, Any], mode: CostMode) -> Optional[UsageEntry]:
        '''Map raw data to UsageEntry - compatibility interface.'''
        if not self._has_valid_tokens(data.get('tokens', {})):
            return None

        timestamp = self._extract_timestamp(data)
        if timestamp is None:
            return None

        model = self._extract_model(data)
        metadata = self._extract_metadata(data)

        usage_entry = UsageEntry(
            timestamp=timestamp,
            model=model,
            metadata=metadata,
            cost=0.0  # Placeholder cost, to be calculated
        )

        usage_entry.cost = self.pricing_calculator.calculate_cost(usage_entry)
        return usage_entry

    def _has_valid_tokens(self, tokens: Dict[str, int]) -> bool:
        '''Check if tokens are valid (for test compatibility).'''
        return all(value >= 0 for value in tokens.values())

    def _extract_timestamp(self, data: Dict[str, Any]) -> Optional[datetime]:
        '''Extract timestamp (for test compatibility).'''
        timestamp = data.get('timestamp')
        if isinstance(timestamp, str):
            try:
                return self.timezone_handler.convert_to_utc(datetime.fromisoformat(timestamp))
            except ValueError:
                return None
        return None

    def _extract_model(self, data: Dict[str, Any]) -> str:
        '''Extract model name (for test compatibility).'''
        return data.get('model', 'unknown')

    def _extract_metadata(self, data: Dict[str, Any]) -> Dict[str, str]:
        '''Extract metadata (for test compatibility).'''
        return data.get('metadata', {})
