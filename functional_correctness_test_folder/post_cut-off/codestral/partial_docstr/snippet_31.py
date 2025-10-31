
from typing import List, Dict, Any, Callable, Optional
from datetime import datetime
import pytz


class UsageAggregator:

    def __init__(self, data_path: str, aggregation_mode: str = 'daily', timezone: str = 'UTC'):
        self.data_path = data_path
        self.aggregation_mode = aggregation_mode
        self.timezone = pytz.timezone(timezone)

    def _aggregate_by_period(self, entries: List[UsageEntry], period_key_func: Callable[[datetime], str], period_type: str, start_date: Optional[datetime] = None, end_date: Optional[datetime] = None) -> List[Dict[str, Any]]:
        aggregated_data = {}
        for entry in entries:
            if start_date and entry.timestamp < start_date:
                continue
            if end_date and entry.timestamp > end_date:
                continue
            period_key = period_key_func(entry.timestamp)
            if period_key not in aggregated_data:
                aggregated_data[period_key] = {
                    'period': period_key,
                    'total_usage': 0,
                    'count': 0,
                    'average_usage': 0
                }
            aggregated_data[period_key]['total_usage'] += entry.usage
            aggregated_data[period_key]['count'] += 1
            aggregated_data[period_key]['average_usage'] = aggregated_data[period_key]['total_usage'] / \
                aggregated_data[period_key]['count']
        return list(aggregated_data.values())

    def aggregate_daily(self, entries: List[UsageEntry], start_date: Optional[datetime] = None, end_date: Optional[datetime] = None) -> List[Dict[str, Any]]:
        def period_key_func(timestamp: datetime) -> str:
            return timestamp.astimezone(self.timezone).strftime('%Y-%m-%d')
        return self._aggregate_by_period(entries, period_key_func, 'date', start_date, end_date)

    def aggregate_monthly(self, entries: List[UsageEntry], start_date: Optional[datetime] = None, end_date: Optional[datetime] = None) -> List[Dict[str, Any]]:
        def period_key_func(timestamp: datetime) -> str:
            return timestamp.astimezone(self.timezone).strftime('%Y-%m')
        return self._aggregate_by_period(entries, period_key_func, 'month', start_date, end_date)

    def aggregate_from_blocks(self, blocks: List[SessionBlock], view_type: str = 'daily') -> List[Dict[str, Any]]:
        entries = []
        for block in blocks:
            entries.extend(block.entries)
        if view_type == 'daily':
            return self.aggregate_daily(entries)
        elif view_type == 'monthly':
            return self.aggregate_monthly(entries)
        else:
            raise ValueError(
                "Invalid view_type. Must be 'daily' or 'monthly'.")

    def calculate_totals(self, aggregated_data: List[Dict[str, Any]]) -> Dict[str, Any]:
        total_usage = sum(item['total_usage'] for item in aggregated_data)
        total_count = sum(item['count'] for item in aggregated_data)
        average_usage = total_usage / total_count if total_count else 0
        return {
            'total_usage': total_usage,
            'total_count': total_count,
            'average_usage': average_usage
        }

    def aggregate(self) -> List[Dict[str, Any]]:
        entries = self._read_data()
        if self.aggregation_mode == 'daily':
            return self.aggregate_daily(entries)
        elif self.aggregation_mode == 'monthly':
            return self.aggregate_monthly(entries)
        else:
            raise ValueError(
                "Invalid aggregation_mode. Must be 'daily' or 'monthly'.")

    def _read_data(self) -> List[UsageEntry]:
        # Implement data reading logic here
        pass


class UsageEntry:
    def __init__(self, timestamp: datetime, usage: float):
        self.timestamp = timestamp
        self.usage = usage


class SessionBlock:
    def __init__(self, entries: List[UsageEntry]):
        self.entries = entries
