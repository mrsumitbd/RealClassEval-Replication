
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
        # Assuming _map_to_usage_entry is a function that maps data to UsageEntry
        # For demonstration purposes, it's implemented here
        def _map_to_usage_entry(data: Dict[str, Any], pricing_calculator: 'PricingCalculator', mode: 'CostMode') -> Optional['UsageEntry']:
            # Implementation of _map_to_usage_entry
            timestamp = self._extract_timestamp(data)
            if timestamp is None:
                return None
            model = self._extract_model(data)
            metadata = self._extract_metadata(data)
            tokens = data.get('tokens', {})
            if not self._has_valid_tokens(tokens):
                return None
            # Calculate cost using pricing_calculator
            cost = self.pricing_calculator.calculate_cost(model, tokens, mode)
            return UsageEntry(timestamp, model, metadata, cost)

        return _map_to_usage_entry(data, self.pricing_calculator, mode)

    def _has_valid_tokens(self, tokens: Dict[str, int]) -> bool:
        '''Check if tokens are valid (for test compatibility).'''
        return all(value >= 0 for value in tokens.values())

    def _extract_timestamp(self, data: Dict[str, Any]) -> Optional[datetime]:
        '''Extract timestamp (for test compatibility).'''
        timestamp = data.get('timestamp')
        if timestamp is None:
            return None
        # Assuming timezone_handler can handle timestamp conversion
        return self.timezone_handler.convert_to_utc(timestamp)

    def _extract_model(self, data: Dict[str, Any]) -> str:
        '''Extract model name (for test compatibility).'''
        return data.get('model', '')

    def _extract_metadata(self, data: Dict[str, Any]) -> Dict[str, str]:
        '''Extract metadata (for test compatibility).'''
        return data.get('metadata', {})
