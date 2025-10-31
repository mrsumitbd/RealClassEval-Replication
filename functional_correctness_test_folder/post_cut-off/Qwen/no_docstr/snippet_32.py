
from typing import Dict, Any, Optional
from datetime import datetime
from enum import Enum


class CostMode(Enum):
    DETAILED = 1
    SUMMARY = 2


class PricingCalculator:
    def calculate_cost(self, model: str, tokens: Dict[str, int]) -> float:
        pass


class TimezoneHandler:
    def convert_to_utc(self, timestamp: datetime) -> datetime:
        pass


class UsageEntry:
    def __init__(self, timestamp: datetime, model: str, metadata: Dict[str, str], cost: float):
        self.timestamp = timestamp
        self.model = model
        self.metadata = metadata
        self.cost = cost


class UsageEntryMapper:

    def __init__(self, pricing_calculator: PricingCalculator, timezone_handler: TimezoneHandler):
        self.pricing_calculator = pricing_calculator
        self.timezone_handler = timezone_handler

    def map(self, data: Dict[str, Any], mode: CostMode) -> Optional[UsageEntry]:
        if not self._has_valid_tokens(data.get('tokens', {})):
            return None

        timestamp = self._extract_timestamp(data)
        if not timestamp:
            return None

        model = self._extract_model(data)
        metadata = self._extract_metadata(data)
        cost = self.pricing_calculator.calculate_cost(
            model, data.get('tokens', {}))

        return UsageEntry(timestamp, model, metadata, cost)

    def _has_valid_tokens(self, tokens: Dict[str, int]) -> bool:
        return all(isinstance(v, int) and v >= 0 for v in tokens.values())

    def _extract_timestamp(self, data: Dict[str, Any]) -> Optional[datetime]:
        timestamp = data.get('timestamp')
        if isinstance(timestamp, str):
            try:
                dt = datetime.fromisoformat(timestamp)
                return self.timezone_handler.convert_to_utc(dt)
            except ValueError:
                return None
        return None

    def _extract_model(self, data: Dict[str, Any]) -> str:
        return data.get('model', 'unknown')

    def _extract_metadata(self, data: Dict[str, Any]) -> Dict[str, str]:
        return data.get('metadata', {})
