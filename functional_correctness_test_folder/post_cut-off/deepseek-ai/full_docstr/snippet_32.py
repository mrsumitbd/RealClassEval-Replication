
class UsageEntryMapper:
    '''Compatibility wrapper for legacy UsageEntryMapper interface.
    This class provides backward compatibility for tests that expect
    the old UsageEntryMapper interface, wrapping the new functional
    approach in _map_to_usage_entry.
    '''

    def __init__(self, pricing_calculator: PricingCalculator, timezone_handler: TimezoneHandler):
        '''Initialize with required components.'''
        self._pricing_calculator = pricing_calculator
        self._timezone_handler = timezone_handler

    def map(self, data: Dict[str, Any], mode: CostMode) -> Optional[UsageEntry]:
        '''Map raw data to UsageEntry - compatibility interface.'''
        tokens = data.get('tokens', {})
        if not self._has_valid_tokens(tokens):
            return None

        timestamp = self._extract_timestamp(data)
        if timestamp is None:
            return None

        model = self._extract_model(data)
        metadata = self._extract_metadata(data)

        cost = self._pricing_calculator.calculate_cost(tokens, mode)
        if cost is None:
            return None

        return UsageEntry(
            timestamp=timestamp,
            model=model,
            tokens=tokens,
            cost=cost,
            metadata=metadata
        )

    def _has_valid_tokens(self, tokens: Dict[str, int]) -> bool:
        '''Check if tokens are valid (for test compatibility).'''
        return isinstance(tokens, dict) and all(
            isinstance(k, str) and isinstance(v, int) and v >= 0
            for k, v in tokens.items()
        )

    def _extract_timestamp(self, data: Dict[str, Any]) -> Optional[datetime]:
        '''Extract timestamp (for test compatibility).'''
        timestamp = data.get('timestamp')
        if timestamp is None:
            return None
        if isinstance(timestamp, datetime):
            return self._timezone_handler.normalize(timestamp)
        return None

    def _extract_model(self, data: Dict[str, Any]) -> str:
        '''Extract model name (for test compatibility).'''
        return data.get('model', 'unknown')

    def _extract_metadata(self, data: Dict[str, Any]) -> Dict[str, str]:
        '''Extract metadata (for test compatibility).'''
        return data.get('metadata', {})
