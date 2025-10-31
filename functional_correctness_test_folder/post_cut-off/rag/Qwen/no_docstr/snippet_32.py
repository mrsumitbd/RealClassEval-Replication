
from typing import Any, Dict, Optional
from datetime import datetime


class UsageEntryMapper:
    '''Compatibility wrapper for legacy UsageEntryMapper interface.
    This class provides backward compatibility for tests that expect
    the old UsageEntryMapper interface, wrapping the new functional
    approach in _map_to_usage_entry.
    '''

    def __init__(self, pricing_calculator: 'PricingCalculator', timezone_handler: 'TimezoneHandler'):
        '''Initialize with required components.'''
        self.pricing_calculator = pricing_calculator
        self.timezone_handler = timezone_handler

    def map(self, data: Dict[str, Any], mode: 'CostMode') -> Optional['UsageEntry']:
        '''Map raw data to UsageEntry - compatibility interface.'''
        if not self._has_valid_tokens(data.get('tokens', {})):
            return None

        timestamp = self._extract_timestamp(data)
        if timestamp is None:
            return None

        model = self._extract_model(data)
        metadata = self._extract_metadata(data)

        return self._map_to_usage_entry(data, timestamp, model, metadata, mode)

    def _has_valid_tokens(self, tokens: Dict[str, int]) -> bool:
        '''Check if tokens are valid (for test compatibility).'''
        return all(isinstance(v, int) and v >= 0 for v in tokens.values())

    def _extract_timestamp(self, data: Dict[str, Any]) -> Optional[datetime]:
        '''Extract timestamp (for test compatibility).'''
        timestamp_str = data.get('timestamp')
        if timestamp_str:
            try:
                return self.timezone_handler.parse_timestamp(timestamp_str)
            except ValueError:
                return None
        return None

    def _extract_model(self, data: Dict[str, Any]) -> str:
        '''Extract model name (for test compatibility).'''
        return data.get('model', 'unknown')

    def _extract_metadata(self, data: Dict[str, Any]) -> Dict[str, str]:
        '''Extract metadata (for test compatibility).'''
        return data.get('metadata', {})

    def _map_to_usage_entry(self, data: Dict[str, Any], timestamp: datetime, model: str, metadata: Dict[str, str], mode: 'CostMode') -> 'UsageEntry':
        '''Map data to UsageEntry using the new functional approach.'''
        cost = self.pricing_calculator.calculate_cost(
            data['tokens'], model, mode)
        return UsageEntry(timestamp=timestamp, model=model, cost=cost, metadata=metadata)


class PricingCalculator:
    def calculate_cost(self, tokens: Dict[str, int], model: str, mode: 'CostMode') -> float:
        # Dummy implementation for demonstration
        return sum(tokens.values()) * 0.01


class TimezoneHandler:
    def parse_timestamp(self, timestamp_str: str) -> datetime:
        # Dummy implementation for demonstration
        from dateutil import parser
        return parser.parse(timestamp_str)


class CostMode:
    # Dummy implementation for demonstration
    def __init__(self, mode: str):
        self.mode = mode


class UsageEntry:
    def __init__(self, timestamp: datetime, model: str, cost: float, metadata: Dict[str, str]):
        self.timestamp = timestamp
        self.model = model
        self.cost = cost
        self.metadata = metadata
