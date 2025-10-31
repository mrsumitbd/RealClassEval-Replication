
from typing import Dict, Any, Optional
from datetime import datetime


class UsageEntryMapper:

    def __init__(self, pricing_calculator: PricingCalculator, timezone_handler: TimezoneHandler):
        self.pricing_calculator = pricing_calculator
        self.timezone_handler = timezone_handler

    def map(self, data: Dict[str, Any], mode: CostMode) -> Optional[UsageEntry]:
        if not self._has_valid_tokens(data.get('tokens', {})):
            return None

        timestamp = self._extract_timestamp(data)
        if timestamp is None:
            return None

        model = self._extract_model(data)
        metadata = self._extract_metadata(data)

        cost = self.pricing_calculator.calculate_cost(data['tokens'], mode)

        return UsageEntry(
            timestamp=timestamp,
            model=model,
            tokens=data['tokens'],
            cost=cost,
            metadata=metadata
        )

    def _has_valid_tokens(self, tokens: Dict[str, int]) -> bool:
        return isinstance(tokens, dict) and all(
            isinstance(k, str) and isinstance(v, int) and v >= 0
            for k, v in tokens.items()
        )

    def _extract_timestamp(self, data: Dict[str, Any]) -> Optional[datetime]:
        timestamp = data.get('timestamp')
        if timestamp is None:
            return None
        if isinstance(timestamp, datetime):
            return self.timezone_handler.normalize(timestamp)
        try:
            parsed_timestamp = datetime.fromisoformat(timestamp)
            return self.timezone_handler.normalize(parsed_timestamp)
        except (TypeError, ValueError):
            return None

    def _extract_model(self, data: Dict[str, Any]) -> str:
        return data.get('model', 'unknown')

    def _extract_metadata(self, data: Dict[str, Any]) -> Dict[str, str]:
        return data.get('metadata', {})
