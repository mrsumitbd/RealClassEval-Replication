
from typing import Dict, Any, Optional
from datetime import datetime


class UsageEntryMapper:

    def __init__(self, pricing_calculator: 'PricingCalculator', timezone_handler: 'TimezoneHandler'):
        self.pricing_calculator = pricing_calculator
        self.timezone_handler = timezone_handler

    def map(self, data: Dict[str, Any], mode: 'CostMode') -> Optional['UsageEntry']:
        timestamp = self._extract_timestamp(data)
        if timestamp is None:
            return None

        model = self._extract_model(data)
        metadata = self._extract_metadata(data)
        tokens = data.get('tokens', {})

        if not self._has_valid_tokens(tokens):
            return None

        usage_entry = UsageEntry(
            timestamp=timestamp,
            model=model,
            input_tokens=tokens.get('input', 0),
            output_tokens=tokens.get('output', 0),
            metadata=metadata
        )

        usage_entry.cost = self.pricing_calculator.calculate(usage_entry, mode)
        return usage_entry

    def _has_valid_tokens(self, tokens: Dict[str, int]) -> bool:
        return 'input' in tokens and 'output' in tokens and tokens['input'] >= 0 and tokens['output'] >= 0

    def _extract_timestamp(self, data: Dict[str, Any]) -> Optional[datetime]:
        timestamp = data.get('timestamp')
        if timestamp is None:
            return None
        return self.timezone_handler.convert_to_utc(timestamp)

    def _extract_model(self, data: Dict[str, Any]) -> str:
        return data.get('model', '')

    def _extract_metadata(self, data: Dict[str, Any]) -> Dict[str, str]:
        metadata = data.get('metadata', {})
        return {k: str(v) for k, v in metadata.items()}
