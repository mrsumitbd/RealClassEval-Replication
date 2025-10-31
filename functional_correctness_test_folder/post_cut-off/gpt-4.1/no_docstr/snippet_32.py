
from typing import Dict, Any, Optional
from datetime import datetime


class UsageEntryMapper:

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

        cost = self.pricing_calculator.calculate_cost(model, tokens, mode)
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
        if not isinstance(tokens, dict):
            return False
        for key in ['prompt', 'completion']:
            if key not in tokens or not isinstance(tokens[key], int) or tokens[key] < 0:
                return False
        return True

    def _extract_timestamp(self, data: Dict[str, Any]) -> Optional[datetime]:
        ts = data.get('timestamp')
        if ts is None:
            return None
        if isinstance(ts, datetime):
            return self.timezone_handler.normalize(ts)
        try:
            # Assume ISO format string
            dt = datetime.fromisoformat(ts)
            return self.timezone_handler.normalize(dt)
        except Exception:
            return None

    def _extract_model(self, data: Dict[str, Any]) -> str:
        return str(data.get('model', 'unknown'))

    def _extract_metadata(self, data: Dict[str, Any]) -> Dict[str, str]:
        meta = data.get('metadata', {})
        if not isinstance(meta, dict):
            return {}
        return {str(k): str(v) for k, v in meta.items()}
