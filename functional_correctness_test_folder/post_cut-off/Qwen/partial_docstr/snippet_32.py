
from typing import Dict, Any, Optional
from datetime import datetime
from enum import Enum


class PricingCalculator:
    def calculate_cost(self, usage_entry: 'UsageEntry') -> float:
        pass


class TimezoneHandler:
    def convert_to_utc(self, timestamp: datetime) -> datetime:
        pass


class CostMode(Enum):
    DETAILED = 1
    SUMMARY = 2


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
        self.pricing_calculator = pricing_calculator
        self.timezone_handler = timezone_handler

    def map(self, data: Dict[str, Any], mode: CostMode) -> Optional[UsageEntry]:
        if not self._has_valid_tokens(data.get('tokens', {})):
            return None
        timestamp = self._extract_timestamp(data)
        if timestamp is None:
            return None
        model = self._extract_model(data)
        metadata = self._extract_metadata(data)
        usage_entry = UsageEntry(timestamp, model, metadata, 0.0)
        usage_entry.cost = self.pricing_calculator.calculate_cost(usage_entry)
        return usage_entry

    def _has_valid_tokens(self, tokens: Dict[str, int]) -> bool:
        return all(count > 0 for count in tokens.values())

    def _extract_timestamp(self, data: Dict[str, Any]) -> Optional[datetime]:
        timestamp = data.get('timestamp')
        if isinstance(timestamp, str):
            try:
                dt = datetime.fromisoformat(timestamp)
                return self.timezone_handler.convert_to_utc(dt)
            except ValueError:
                return None
        return None

    def _extract_model(self, data: Dict[str, Any]) -> str:
        '''Extract model name (for test compatibility).'''
        return data.get('model', 'unknown')

    def _extract_metadata(self, data: Dict[str, Any]) -> Dict[str, str]:
        return data.get('metadata', {})
