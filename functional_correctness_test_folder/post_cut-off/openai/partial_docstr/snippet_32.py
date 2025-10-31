
from datetime import datetime
from typing import Any, Dict, Optional


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
        return self._map_to_usage_entry(data, mode)

    def _has_valid_tokens(self, tokens: Dict[str, int]) -> bool:
        required = ('prompt_tokens', 'completion_tokens', 'total_tokens')
        for key in required:
            if key not in tokens:
                return False
            val = tokens[key]
            if not isinstance(val, int) or val < 0:
                return False
        return True

    def _extract_timestamp(self, data: Dict[str, Any]) -> Optional[datetime]:
        ts = data.get('timestamp')
        if ts is None:
            return None
        # Try ISO format
        if isinstance(ts, str):
            try:
                dt = datetime.fromisoformat(ts)
            except ValueError:
                return None
        # Try epoch seconds
        elif isinstance(ts, (int, float)):
            try:
                dt = datetime.fromtimestamp(ts)
            except (OSError, OverflowError):
                return None
        else:
            return None
        # Convert to local timezone
        return self.timezone_handler.to_local(dt)

    def _extract_model(self, data: Dict[str, Any]) -> str:
        '''Extract model name (for test compatibility).'''
        return str(data.get('model', ''))

    def _extract_metadata(self, data: Dict[str, Any]) -> Dict[str, str]:
        meta = data.get('metadata', {})
        if not isinstance(meta, dict):
            return {}
        return {k: str(v) for k, v in meta.items()}

    def _map_to_usage_entry(self, data: Dict[str, Any], mode: 'CostMode') -> Optional['UsageEntry']:
        # Extract tokens
        usage = data.get('usage')
        if not isinstance(usage, dict):
            return None
        tokens = {
            'prompt_tokens': usage.get('prompt_tokens'),
            'completion_tokens': usage.get('completion_tokens'),
            'total_tokens': usage.get('total_tokens')
        }
        if not self._has_valid_tokens(tokens):
            return None

        # Extract timestamp
        timestamp = self._extract_timestamp(data)
        if timestamp is None:
            return None

        # Extract model
        model = self._extract_model(data)

        # Extract metadata
        metadata = self._extract_metadata(data)

        # Calculate cost
        cost = self.pricing_calculator.calculate(
            prompt_tokens=tokens['prompt_tokens'],
            completion_tokens=tokens['completion_tokens'],
            model=model,
            mode=mode
        )

        # Build UsageEntry
        return UsageEntry(
            timestamp=timestamp,
            model=model,
            prompt_tokens=tokens['prompt_tokens'],
            completion_tokens=tokens['completion_tokens'],
            total_tokens=tokens['total_tokens'],
            cost=cost,
            metadata=metadata
        )
