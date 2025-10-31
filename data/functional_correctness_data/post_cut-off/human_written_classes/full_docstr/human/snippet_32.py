from claude_monitor.core.pricing import PricingCalculator
from datetime import datetime, timedelta
from claude_monitor.utils.time_utils import TimezoneHandler
from claude_monitor.core.models import CostMode, UsageEntry
from typing import Any, Dict, List, Optional, Set, Tuple
from claude_monitor.core.data_processors import DataConverter, TimestampProcessor, TokenExtractor

class UsageEntryMapper:
    """Compatibility wrapper for legacy UsageEntryMapper interface.

    This class provides backward compatibility for tests that expect
    the old UsageEntryMapper interface, wrapping the new functional
    approach in _map_to_usage_entry.
    """

    def __init__(self, pricing_calculator: PricingCalculator, timezone_handler: TimezoneHandler):
        """Initialize with required components."""
        self.pricing_calculator = pricing_calculator
        self.timezone_handler = timezone_handler

    def map(self, data: Dict[str, Any], mode: CostMode) -> Optional[UsageEntry]:
        """Map raw data to UsageEntry - compatibility interface."""
        return _map_to_usage_entry(data, mode, self.timezone_handler, self.pricing_calculator)

    def _has_valid_tokens(self, tokens: Dict[str, int]) -> bool:
        """Check if tokens are valid (for test compatibility)."""
        return any((v > 0 for v in tokens.values()))

    def _extract_timestamp(self, data: Dict[str, Any]) -> Optional[datetime]:
        """Extract timestamp (for test compatibility)."""
        if 'timestamp' not in data:
            return None
        processor = TimestampProcessor(self.timezone_handler)
        return processor.parse_timestamp(data['timestamp'])

    def _extract_model(self, data: Dict[str, Any]) -> str:
        """Extract model name (for test compatibility)."""
        return DataConverter.extract_model_name(data, default='unknown')

    def _extract_metadata(self, data: Dict[str, Any]) -> Dict[str, str]:
        """Extract metadata (for test compatibility)."""
        message = data.get('message', {})
        return {'message_id': data.get('message_id') or message.get('id', ''), 'request_id': data.get('request_id') or data.get('requestId', 'unknown')}