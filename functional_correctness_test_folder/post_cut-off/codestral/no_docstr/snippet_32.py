
from datetime import datetime
from typing import Dict, Any, Optional


class UsageEntryMapper:

    def __init__(self, pricing_calculator: PricingCalculator, timezone_handler: TimezoneHandler):

        self.pricing_calculator = pricing_calculator
        self.timezone_handler = timezone_handler

    def map(self, data: Dict[str, Any], mode: CostMode) -> Optional[UsageEntry]:

        timestamp = self._extract_timestamp(data)
        if not timestamp:
            return None

        model = self._extract_model(data)
        tokens = data.get('tokens', {})
        if not self._has_valid_tokens(tokens):
            return None

        metadata = self._extract_metadata(data)
        cost = self.pricing_calculator.calculate_cost(tokens, model, mode)

        return UsageEntry(
            timestamp=timestamp,
            model=model,
            tokens=tokens,
            metadata=metadata,
            cost=cost
        )

    def _has_valid_tokens(self, tokens: Dict[str, int]) -> bool:

        return all(isinstance(value, int) and value >= 0 for value in tokens.values())

    def _extract_timestamp(self, data: Dict[str, Any]) -> Optional[datetime]:

        timestamp_str = data.get('timestamp')
        if not timestamp_str:
            return None

        try:
            timestamp = datetime.fromisoformat(timestamp_str)
            return self.timezone_handler.convert_to_utc(timestamp)
        except ValueError:
            return None

    def _extract_model(self, data: Dict[str, Any]) -> str:

        return data.get('model', 'unknown')

    def _extract_metadata(self, data: Dict[str, Any]) -> Dict[str, str]:

        metadata = data.get('metadata', {})
        return {key: str(value) for key, value in metadata.items()}
