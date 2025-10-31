import json
from datetime import datetime
from typing import Any, Dict, Optional


class UsageEntryMapper:
    '''Compatibility wrapper for legacy UsageEntryMapper interface.
    This class provides backward compatibility for tests that expect
    the old UsageEntryMapper interface, wrapping the new functional
    approach in _map_to_usage_entry.
    '''

    def __init__(self, pricing_calculator: Any, timezone_handler: Any):
        '''Initialize with required components.'''
        self.pricing_calculator = pricing_calculator
        self.timezone_handler = timezone_handler

    def map(self, data: Dict[str, Any], mode: Any) -> Optional[Any]:
        '''Map raw data to UsageEntry - compatibility interface.'''
        return self._map_to_usage_entry(data, mode)

    def _has_valid_tokens(self, tokens: Dict[str, int]) -> bool:
        '''Check if tokens are valid (for test compatibility).'''
        if not isinstance(tokens, dict):
            return False
        for key, value in tokens.items():
            if not isinstance(value, int) or value < 0:
                return False
        return True

    def _extract_timestamp(self, data: Dict[str, Any]) -> Optional[datetime]:
        '''Extract timestamp (for test compatibility).'''
        ts = data.get('timestamp')
        if ts is None:
            return None
        if isinstance(ts, datetime):
            return ts
        try:
            # Try ISO format first
            dt = datetime.fromisoformat(ts)
            # Convert to UTC if timezone handler available
            if hasattr(self.timezone_handler, 'to_utc'):
                return self.timezone_handler.to_utc(dt)
            return dt
        except Exception:
            return None

    def _extract_model(self, data: Dict[str, Any]) -> str:
        '''Extract model name (for test compatibility).'''
        return data.get('model', '')

    def _extract_metadata(self, data: Dict[str, Any]) -> Dict[str, str]:
        '''Extract metadata (for test compatibility).'''
        meta = data.get('metadata', {})
        if isinstance(meta, dict):
            return {str(k): str(v) for k, v in meta.items()}
        return {}

    def _map_to_usage_entry(self, data: Dict[str, Any], mode: Any) -> Optional[Any]:
        '''Internal mapping logic using the new functional approach.'''
        # Extract required fields
        timestamp = self._extract_timestamp(data)
        model = self._extract_model(data)
        metadata = self._extract_metadata(data)
        tokens = data.get('tokens', {})
        if not self._has_valid_tokens(tokens):
            return None

        # Calculate cost using pricing calculator
        try:
            cost = self.pricing_calculator.calculate_cost(tokens, mode)
        except Exception:
            cost = None

        # Build a simple dict representing UsageEntry
        usage_entry = {
            'timestamp': timestamp,
            'model': model,
            'metadata': metadata,
            'tokens': tokens,
            'cost': cost
        }
        return usage_entry

    def __str__(self) -> str:
        return json.dumps({
            'pricing_calculator': str(self.pricing_calculator),
            'timezone_handler': str(self.timezone_handler)
        }, indent=2)

    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, UsageEntryMapper):
            return False
        return (self.pricing_calculator == other.pricing_calculator and
                self.timezone_handler == other.timezone_handler)

    def __ne__(self, other: Any) -> bool:
        return not self == other
