
from typing import Dict, Any, Optional
from datetime import datetime


class UsageEntryMapper:
    '''Compatibility wrapper for legacy UsageEntryMapper interface.
    This class provides backward compatibility for tests that expect
    the old UsageEntryMapper interface, wrapping the new functional
    approach in _map_to_usage_entry.
    '''

    def __init__(self, pricing_calculator: 'PricingCalculator', timezone_handler: 'TimezoneHandler'):
        self.pricing_calculator = pricing_calculator
        self.timezone_handler = timezone_handler

    def map(self, data: Dict[str, Any], mode: 'CostMode') -> Optional['UsageEntry']:
        timestamp = self._extract_timestamp(data)
        if timestamp is None:
            return None

        model = self._extract_model(data)
        metadata = self._extract_metadata(data)
        tokens = data.get('tokens', {})

        if not self._has_valid_tokens(tokens):
            return None

        usage_entry = self.pricing_calculator._map_to_usage_entry(
            data, mode, timestamp, model, metadata)
        return usage_entry

    def _has_valid_tokens(self, tokens: Dict[str, int]) -> bool:
        return all(value > 0 for value in tokens.values())

    def _extract_timestamp(self, data: Dict[str, Any]) -> Optional[datetime]:
        timestamp = data.get('timestamp')
        if timestamp is None:
            return None
        return self.timezone_handler.parse_timestamp(timestamp)

    def _extract_model(self, data: Dict[str, Any]) -> str:
        '''Extract model name (for test compatibility).'''
        return data.get('model', '')

    def _extract_metadata(self, data: Dict[str, Any]) -> Dict[str, str]:
        metadata = data.get('metadata', {})
        return {key: str(value) for key, value in metadata.items()}
