
from typing import Dict, Any, Optional
from datetime import datetime


class UsageEntryMapper:
    """
    Compatibility wrapper for legacy UsageEntryMapper interface.
    This class provides backward compatibility for tests that expect
    the old UsageEntryMapper interface, wrapping the new functional
    approach in _map_to_usage_entry.
    """

    def __init__(self, pricing_calculator: 'PricingCalculator', timezone_handler: 'TimezoneHandler'):
        """
        Initialize with required components.
        """
        self.pricing_calculator = pricing_calculator
        self.timezone_handler = timezone_handler

    def map(self, data: Dict[str, Any], mode: 'CostMode') -> Optional['UsageEntry']:
        """
        Map raw data to UsageEntry - compatibility interface.
        """
        # Assuming _map_to_usage_entry is a function that maps raw data to UsageEntry
        from your_module import _map_to_usage_entry
        return _map_to_usage_entry(data, mode, self.pricing_calculator, self.timezone_handler)

    def _has_valid_tokens(self, tokens: Dict[str, int]) -> bool:
        """
        Check if tokens are valid (for test compatibility).
        """
        # Assuming a token is valid if its count is greater than 0
        return all(count > 0 for count in tokens.values())

    def _extract_timestamp(self, data: Dict[str, Any]) -> Optional[datetime]:
        """
        Extract timestamp (for test compatibility).
        """
        # Assuming the timestamp is stored in the 'timestamp' key
        timestamp = data.get('timestamp')
        if timestamp is not None:
            return datetime.fromisoformat(timestamp)
        return None

    def _extract_model(self, data: Dict[str, Any]) -> str:
        """
        Extract model name (for test compatibility).
        """
        # Assuming the model name is stored in the 'model' key
        return data.get('model', '')

    def _extract_metadata(self, data: Dict[str, Any]) -> Dict[str, str]:
        """
        Extract metadata (for test compatibility).
        """
        # Assuming metadata is stored in the 'metadata' key
        return data.get('metadata', {})
