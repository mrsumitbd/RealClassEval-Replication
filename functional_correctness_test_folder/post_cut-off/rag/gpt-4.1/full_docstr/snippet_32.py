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
        return _map_to_usage_entry(
            data,
            mode,
            self.pricing_calculator,
            self.timezone_handler
        )

    def _has_valid_tokens(self, tokens: Dict[str, int]) -> bool:
        '''Check if tokens are valid (for test compatibility).'''
        if not tokens or not isinstance(tokens, dict):
            return False
        for v in tokens.values():
            if not isinstance(v, int) or v < 0:
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
            # Try parsing ISO format
            return datetime.fromisoformat(ts)
        except Exception:
            return None

    def _extract_model(self, data: Dict[str, Any]) -> str:
        '''Extract model name (for test compatibility).'''
        return data.get('model', '')

    def _extract_metadata(self, data: Dict[str, Any]) -> Dict[str, str]:
        '''Extract metadata (for test compatibility).'''
        meta = data.get('metadata', {})
        if not isinstance(meta, dict):
            return {}
        # Ensure all keys/values are strings
        return {str(k): str(v) for k, v in meta.items()}

# Note: _map_to_usage_entry, PricingCalculator, TimezoneHandler, CostMode, UsageEntry
# are assumed to be defined elsewhere.
