
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
        tokens = data.get('tokens', {})
        if not self._has_valid_tokens(tokens):
            return None
        timestamp = self._extract_timestamp(data)
        if timestamp is None:
            return None
        model = self._extract_model(data)
        metadata = self._extract_metadata(data)
        cost = self.pricing_calculator.calculate(tokens, model, mode)
        local_time = self.timezone_handler.to_local(timestamp)
        return UsageEntry(
            timestamp=local_time,
            model=model,
            tokens=tokens,
            cost=cost,
            metadata=metadata
        )

    def _has_valid_tokens(self, tokens: Dict[str, int]) -> bool:
        if not isinstance(tokens, dict):
            return False
        for v in tokens.values():
            if not isinstance(v, int) or v < 0:
                return False
        return bool(tokens)

    def _extract_timestamp(self, data: Dict[str, Any]) -> Optional[datetime]:
        ts = data.get('timestamp')
        if isinstance(ts, datetime):
            return ts
        if isinstance(ts, str):
            try:
                return datetime.fromisoformat(ts)
            except Exception:
                return None
        return None

    def _extract_model(self, data: Dict[str, Any]) -> str:
        return data.get('model', '')

    def _extract_metadata(self, data: Dict[str, Any]) -> Dict[str, str]:
        meta = data.get('metadata', {})
        if not isinstance(meta, dict):
            return {}
        return {str(k): str(v) for k, v in meta.items()}
