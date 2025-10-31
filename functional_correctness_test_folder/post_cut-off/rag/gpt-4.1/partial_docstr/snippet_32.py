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
        return self._map_to_usage_entry(data, mode)

    def _map_to_usage_entry(self, data: Dict[str, Any], mode: 'CostMode') -> Optional['UsageEntry']:
        # This is a placeholder for the actual mapping logic.
        # For compatibility, we assume UsageEntry has a from_dict or similar constructor.
        # The actual implementation would depend on UsageEntry and pricing_calculator.
        # Here, we just show a typical pattern.
        tokens = data.get('tokens', {})
        if not self._has_valid_tokens(tokens):
            return None
        timestamp = self._extract_timestamp(data)
        model = self._extract_model(data)
        metadata = self._extract_metadata(data)
        cost = self.pricing_calculator.calculate_cost(tokens, model, mode)
        # UsageEntry is assumed to have a constructor like UsageEntry(...)
        return UsageEntry(
            tokens=tokens,
            timestamp=timestamp,
            model=model,
            metadata=metadata,
            cost=cost
        )

    def _has_valid_tokens(self, tokens: Dict[str, int]) -> bool:
        '''Check if tokens are valid (for test compatibility).'''
        if not isinstance(tokens, dict):
            return False
        for v in tokens.values():
            if not isinstance(v, int) or v < 0:
                return False
        return bool(tokens)

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
        return {str(k): str(v) for k, v in meta.items()}
