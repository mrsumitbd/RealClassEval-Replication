
from typing import Dict, Any, Optional
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
        usage_entry = self._map_to_usage_entry(data, mode)
        return usage_entry

    def _map_to_usage_entry(self, data: Dict[str, Any], mode: 'CostMode') -> Optional['UsageEntry']:
        # Extract required fields
        tokens = data.get('tokens', {})
        if not self._has_valid_tokens(tokens):
            return None
        timestamp = self._extract_timestamp(data)
        if not timestamp:
            return None
        model = self._extract_model(data)
        metadata = self._extract_metadata(data)
        cost = self.pricing_calculator.calculate(model, tokens, mode)
        # UsageEntry is assumed to be a dataclass or similar
        return UsageEntry(
            timestamp=timestamp,
            model=model,
            tokens=tokens,
            cost=cost,
            metadata=metadata
        )

    def _has_valid_tokens(self, tokens: Dict[str, int]) -> bool:
        '''Check if tokens are valid (for test compatibility).'''
        if not isinstance(tokens, dict):
            return False
        for k, v in tokens.items():
            if not isinstance(k, str) or not isinstance(v, int) or v < 0:
                return False
        return bool(tokens)

    def _extract_timestamp(self, data: Dict[str, Any]) -> Optional[datetime]:
        '''Extract timestamp (for test compatibility).'''
        ts = data.get('timestamp')
        if isinstance(ts, datetime):
            return self.timezone_handler.normalize(ts)
        elif isinstance(ts, str):
            try:
                dt = datetime.fromisoformat(ts)
                return self.timezone_handler.normalize(dt)
            except Exception:
                return None
        return None

    def _extract_model(self, data: Dict[str, Any]) -> str:
        '''Extract model name (for test compatibility).'''
        return data.get('model', '')

    def _extract_metadata(self, data: Dict[str, Any]) -> Dict[str, str]:
        '''Extract metadata (for test compatibility).'''
        meta = data.get('metadata', {})
        if not isinstance(meta, dict):
            return {}
        return {str(k): str(v) for k, v in meta.items()}
