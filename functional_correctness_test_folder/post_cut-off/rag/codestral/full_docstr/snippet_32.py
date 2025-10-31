
from typing import Any, Dict, Optional
from datetime import datetime


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
        if not timestamp:
            return None

        model = self._extract_model(data)
        metadata = self._extract_metadata(data)

        return UsageEntry(
            timestamp=timestamp,
            model=model,
            tokens=data.get('tokens', {}),
            metadata=metadata,
            mode=mode
        )

    def _has_valid_tokens(self, tokens: Dict[str, int]) -> bool:
        '''Check if tokens are valid (for test compatibility).'''
        return all(isinstance(v, int) and v >= 0 for v in tokens.values())

    def _extract_timestamp(self, data: Dict[str, Any]) -> Optional[datetime]:
        '''Extract timestamp (for test compatibility).'''
        timestamp_str = data.get('timestamp')
        if not timestamp_str:
            return None

        try:
            return datetime.fromisoformat(timestamp_str)
        except (ValueError, TypeError):
            return None

    def _extract_model(self, data: Dict[str, Any]) -> str:
        '''Extract model name (for test compatibility).'''
        return data.get('model', 'unknown')

    def _extract_metadata(self, data: Dict[str, Any]) -> Dict[str, str]:
        '''Extract metadata (for test compatibility).'''
        metadata = data.get('metadata', {})
        return {k: str(v) for k, v in metadata.items() if isinstance(v, (str, int, float, bool))}
