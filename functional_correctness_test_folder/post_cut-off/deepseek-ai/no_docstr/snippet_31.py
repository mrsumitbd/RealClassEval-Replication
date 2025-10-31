
from typing import List, Dict, Any, Optional, Callable
from datetime import datetime


class UsageAggregator:

    def __init__(self, data_path: str, aggregation_mode: str = 'daily', timezone: str = 'UTC'):
        self.data_path = data_path
        self.aggregation_mode = aggregation_mode
        self.timezone = timezone

    def _aggregate_by_period(self, entries: List[UsageEntry], period_key_func: Callable[[datetime], str], period_type: str, start_date: Optional[datetime] = None, end_date: Optional[datetime] = None) -> List[Dict[str, Any]]:
        filtered_entries = entries
        if start_date is not None:
            filtered_entries = [
                e for e in filtered_entries if e.timestamp >= start_date]
        if end_date is not None:
            filtered_entries = [
                e for e in filtered_entries if e.timestamp <= end_date]

        aggregated_data = {}
        for entry in filtered_entries:
            period_key = period_key_func(entry.timestamp)
            if period_key not in aggregated_data:
                aggregated_data[period_key] = {
                    'period': period_key,
                    'period_type': period_type,
                    'count': 0,
                    'total_duration': 0,
                    'entries': []
                }
            aggregated_data[period_key]['count'] += 1
            aggregated_data[period_key]['total_duration'] += entry.duration
            aggregated_data[period_key]['entries'].append(entry)

        return list(aggregated_data.values())

    def aggregate_daily(self, entries: List[UsageEntry], start_date: Optional[datetime] = None, end_date: Optional[datetime] = None) -> List[Dict[str, Any]]:
        def daily_key_func(dt: datetime) -> str:
            return dt.strftime('%Y-%m-%d')
        return self._aggregate_by_period(entries, daily_key_func, 'daily', start_date, end_date)

    def aggregate_monthly(self, entries: List[UsageEntry], start_date: Optional[datetime] = None, end_date: Optional[datetime] = None) -> List[Dict[str, Any]]:
        def monthly_key_func(dt: datetime) -> str:
            return dt.strftime('%Y-%m')
        return self._aggregate_by_period(entries, monthly_key_func, 'monthly', start_date, end_date)

    def aggregate_from_blocks(self, blocks: List[SessionBlock], view_type: str = 'daily') -> List[Dict[str, Any]]:
        entries = []
        for block in blocks:
            for entry in block.entries:
                entries.append(entry)

        if view_type == 'daily':
            return self.aggregate_daily(entries)
        elif view_type == 'monthly':
            return self.aggregate_monthly(entries)
        else:
            raise ValueError(f"Unsupported view_type: {view_type}")

    def calculate_totals(self, aggregated_data: List[Dict[str, Any]]) -> Dict[str, Any]:
        total_count = 0
        total_duration = 0
        for period_data in aggregated_data:
            total_count += period_data['count']
            total_duration += period_data['total_duration']

        return {
            'total_count': total_count,
            'total_duration': total_duration,
            'periods': len(aggregated_data)
        }
