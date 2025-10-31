
from typing import List, Dict, Any, Callable, Optional
from datetime import datetime


class UsageAggregator:

    def __init__(self, data_path: str, aggregation_mode: str = 'daily', timezone: str = 'UTC'):
        self.data_path = data_path
        self.aggregation_mode = aggregation_mode
        self.timezone = timezone

    def _aggregate_by_period(self, entries: List[UsageEntry], period_key_func: Callable[[datetime], str], period_type: str, start_date: Optional[datetime] = None, end_date: Optional[datetime] = None) -> List[Dict[str, Any]]:
        aggregated = {}
        for entry in entries:
            timestamp = entry.timestamp
            if start_date and timestamp < start_date:
                continue
            if end_date and timestamp > end_date:
                continue
            period_key = period_key_func(timestamp)
            if period_key not in aggregated:
                aggregated[period_key] = {
                    'period': period_key,
                    'period_type': period_type,
                    'total_usage': 0,
                    'total_sessions': 0,
                    'total_duration': 0
                }
            aggregated[period_key]['total_usage'] += entry.usage
            aggregated[period_key]['total_sessions'] += 1
            aggregated[period_key]['total_duration'] += entry.duration

        return sorted(aggregated.values(), key=lambda x: x['period'])

    def aggregate_daily(self, entries: List[UsageEntry], start_date: Optional[datetime] = None, end_date: Optional[datetime] = None) -> List[Dict[str, Any]]:
        def daily_key(timestamp: datetime) -> str:
            return timestamp.strftime('%Y-%m-%d')
        return self._aggregate_by_period(entries, daily_key, 'date', start_date, end_date)

    def aggregate_monthly(self, entries: List[UsageEntry], start_date: Optional[datetime] = None, end_date: Optional[datetime] = None) -> List[Dict[str, Any]]:
        def monthly_key(timestamp: datetime) -> str:
            return timestamp.strftime('%Y-%m')
        return self._aggregate_by_period(entries, monthly_key, 'month', start_date, end_date)

    def aggregate_from_blocks(self, blocks: List[SessionBlock], view_type: str = 'daily') -> List[Dict[str, Any]]:
        entries = []
        for block in blocks:
            entries.extend(block.usage_entries)
        if view_type == 'daily':
            return self.aggregate_daily(entries)
        elif view_type == 'monthly':
            return self.aggregate_monthly(entries)
        else:
            raise ValueError("Invalid view_type. Must be 'daily' or 'monthly'")

    def calculate_totals(self, aggregated_data: List[Dict[str, Any]]) -> Dict[str, Any]:
        totals = {
            'total_usage': 0,
            'total_sessions': 0,
            'total_duration': 0
        }
        for data in aggregated_data:
            totals['total_usage'] += data['total_usage']
            totals['total_sessions'] += data['total_sessions']
            totals['total_duration'] += data['total_duration']
        return totals

    def aggregate(self) -> List[Dict[str, Any]]:
        entries = self._load_entries()
        if self.aggregation_mode == 'daily':
            return self.aggregate_daily(entries)
        elif self.aggregation_mode == 'monthly':
            return self.aggregate_monthly(entries)
        else:
            raise ValueError(
                "Invalid aggregation_mode. Must be 'daily' or 'monthly'")

    def _load_entries(self) -> List[UsageEntry]:
        # Placeholder for loading entries from data_path
        return []
