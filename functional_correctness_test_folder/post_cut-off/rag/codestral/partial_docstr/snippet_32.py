
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
        if not data:
            return None

        timestamp = self._extract_timestamp(data)
        if not timestamp:
            return None

        model = self._extract_model(data)
        if not model:
            return None

        tokens = data.get('tokens', {})
        if not self._has_valid_tokens(tokens):
            return None

        metadata = self._extract_metadata(data)

        return UsageEntry(
            timestamp=timestamp,
            model=model,
            tokens=tokens,
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
        model = data.get('model')
        if not model:
            return 'unknown'
        return str(model)

    def _extract_metadata(self, data: Dict[str, Any]) -> Dict[str, str]:
        '''Extract metadata (for test compatibility).'''
        metadata = data.get('metadata', {})
        if not isinstance(metadata, dict):
            return {}
        return {str(k): str(v) for k, v in metadata.items()}
