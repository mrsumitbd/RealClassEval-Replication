
from datetime import datetime
from typing import Dict, Any, Optional


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
        if not timestamp:
            return None

        model = self._extract_model(data)
        metadata = self._extract_metadata(data)

        return self._map_to_usage_entry(data, mode, timestamp, model, metadata)

    def _has_valid_tokens(self, tokens: Dict[str, int]) -> bool:
        return all(value > 0 for value in tokens.values())

    def _extract_timestamp(self, data: Dict[str, Any]) -> Optional[datetime]:
        timestamp_str = data.get('timestamp')
        if not timestamp_str:
            return None

        try:
            return datetime.fromisoformat(timestamp_str)
        except ValueError:
            return None

    def _extract_model(self, data: Dict[str, Any]) -> str:
        '''Extract model name (for test compatibility).'''
        return data.get('model', 'unknown')

    def _extract_metadata(self, data: Dict[str, Any]) -> Dict[str, str]:
        metadata = data.get('metadata', {})
        return {k: str(v) for k, v in metadata.items()}

    def _map_to_usage_entry(self, data: Dict[str, Any], mode: CostMode, timestamp: datetime, model: str, metadata: Dict[str, str]) -> UsageEntry:
        # Implement the new functional approach to map data to UsageEntry
        pass
