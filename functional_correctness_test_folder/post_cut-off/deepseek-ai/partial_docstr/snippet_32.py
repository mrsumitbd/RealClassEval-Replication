
class UsageEntryMapper:
    '''Compatibility wrapper for legacy UsageEntryMapper interface.
    This class provides backward compatibility for tests that expect
    the old UsageEntryMapper interface, wrapping the new functional
    approach in _map_to_usage_entry.
    '''

    def __init__(self, pricing_calculator: PricingCalculator, timezone_handler: TimezoneHandler):
        self._pricing_calculator = pricing_calculator
        self._timezone_handler = timezone_handler

    def map(self, data: Dict[str, Any], mode: CostMode) -> Optional[UsageEntry]:
        if not self._has_valid_tokens(data.get('tokens', {})):
            return None

        timestamp = self._extract_timestamp(data)
        if timestamp is None:
            return None

        model = self._extract_model(data)
        metadata = self._extract_metadata(data)

        cost = self._pricing_calculator.calculate_cost(data['tokens'], mode)
        return UsageEntry(
            timestamp=timestamp,
            model=model,
            tokens=data['tokens'],
            cost=cost,
            metadata=metadata
        )

    def _has_valid_tokens(self, tokens: Dict[str, int]) -> bool:
        return isinstance(tokens, dict) and all(
            isinstance(k, str) and isinstance(v, int)
            for k, v in tokens.items()
        )

    def _extract_timestamp(self, data: Dict[str, Any]) -> Optional[datetime]:
        timestamp = data.get('timestamp')
        if timestamp is None:
            return None
        return self._timezone_handler.normalize(timestamp)

    def _extract_model(self, data: Dict[str, Any]) -> str:
        return data.get('model', 'unknown')

    def _extract_metadata(self, data: Dict[str, Any]) -> Dict[str, str]:
        return data.get('metadata', {})
