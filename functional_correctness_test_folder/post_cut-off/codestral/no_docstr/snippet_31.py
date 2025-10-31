
from typing import List, Dict, Any, Callable, Optional
from datetime import datetime
from dataclasses import dataclass


@dataclass
class UsageEntry:
    timestamp: datetime
    value: float


@dataclass
class SessionBlock:
    start_time: datetime
    end_time: datetime
    value: float


class UsageAggregator:

    def __init__(self, data_path: str, aggregation_mode: str = 'daily', timezone: str = 'UTC'):

        self.data_path = data_path
        self.aggregation_mode = aggregation_mode
        self.timezone = timezone

    def _aggregate_by_period(self, entries: List[UsageEntry], period_key_func: Callable[[datetime], str], period_type: str, start_date: Optional[datetime] = None, end_date: Optional[datetime] = None) -> List[Dict[str, Any]]:

        aggregated_data = []
        period_data = {}

        for entry in entries:
            if start_date and entry.timestamp < start_date:
                continue
            if end_date and entry.timestamp > end_date:
                continue

            period_key = period_key_func(entry.timestamp)
            if period_key not in period_data:
                period_data[period_key] = {
                    'period': period_key,
                    'total': 0.0,
                    'count': 0,
                    'average': 0.0
                }

            period_data[period_key]['total'] += entry.value
            period_data[period_key]['count'] += 1
            period_data[period_key]['average'] = period_data[period_key]['total'] / \
                period_data[period_key]['count']

        for period_key in sorted(period_data.keys()):
            aggregated_data.append(period_data[period_key])

        return aggregated_data

    def aggregate_daily(self, entries: List[UsageEntry], start_date: Optional[datetime] = None, end_date: Optional[datetime] = None) -> List[Dict[str, Any]]:

        def daily_key_func(timestamp: datetime) -> str:
            return timestamp.strftime('%Y-%m-%d')

        return self._aggregate_by_period(entries, daily_key_func, 'daily', start_date, end_date)

    def aggregate_monthly(self, entries: List[UsageEntry], start_date: Optional[datetime] = None, end_date: Optional[datetime] = None) -> List[Dict[str, Any]]:

        def monthly_key_func(timestamp: datetime) -> str:
            return timestamp.strftime('%Y-%m')

        return self._aggregate_by_period(entries, monthly_key_func, 'monthly', start_date, end_date)

    def aggregate_from_blocks(self, blocks: List[SessionBlock], view_type: str = 'daily') -> List[Dict[str, Any]]:

        entries = []
        for block in blocks:
            entries.append(UsageEntry(block.start_time, block.value))

        if view_type == 'daily':
            return self.aggregate_daily(entries)
        elif view_type == 'monthly':
            return self.aggregate_monthly(entries)
        else:
            raise ValueError(f"Invalid view_type: {view_type}")

    def calculate_totals(self, aggregated_data: List[Dict[str, Any]]) -> Dict[str, Any]:

        total_value = sum(entry['total'] for entry in aggregated_data)
        total_count = sum(entry['count'] for entry in aggregated_data)
        average_value = total_value / total_count if total_count > 0 else 0.0

        return {
            'total_value': total_value,
            'total_count': total_count,
            'average_value': average_value
        }
