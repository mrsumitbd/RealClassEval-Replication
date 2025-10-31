
from typing import List, Dict, Any, Callable, Optional
from datetime import datetime, timedelta
import pytz


class UsageEntry:
    def __init__(self, timestamp: datetime, value: float):
        self.timestamp = timestamp
        self.value = value


class SessionBlock:
    def __init__(self, start_time: datetime, end_time: datetime, usage_entries: List[UsageEntry]):
        self.start_time = start_time
        self.end_time = end_time
        self.usage_entries = usage_entries


class UsageAggregator:

    def __init__(self, data_path: str, aggregation_mode: str = 'daily', timezone: str = 'UTC'):
        self.data_path = data_path
        self.aggregation_mode = aggregation_mode
        self.timezone = pytz.timezone(timezone)

    def _aggregate_by_period(self, entries: List[UsageEntry], period_key_func: Callable[[datetime], str], period_type: str, start_date: Optional[datetime] = None, end_date: Optional[datetime] = None) -> List[Dict[str, Any]]:
        if start_date:
            start_date = self.timezone.localize(start_date)
        if end_date:
            end_date = self.timezone.localize(end_date)

        aggregated_data = {}
        for entry in entries:
            if start_date and entry.timestamp < start_date:
                continue
            if end_date and entry.timestamp > end_date:
                continue
            period_key = period_key_func(entry.timestamp)
            if period_key not in aggregated_data:
                aggregated_data[period_key] = {
                    'period': period_key, 'total': 0}
            aggregated_data[period_key]['total'] += entry.value

        return list(aggregated_data.values())

    def aggregate_daily(self, entries: List[UsageEntry], start_date: Optional[datetime] = None, end_date: Optional[datetime] = None) -> List[Dict[str, Any]]:
        return self._aggregate_by_period(entries, lambda x: x.strftime('%Y-%m-%d'), 'date', start_date, end_date)

    def aggregate_monthly(self, entries: List[UsageEntry], start_date: Optional[datetime] = None, end_date: Optional[datetime] = None) -> List[Dict[str, Any]]:
        return self._aggregate_by_period(entries, lambda x: x.strftime('%Y-%m'), 'month', start_date, end_date)

    def aggregate_from_blocks(self, blocks: List[SessionBlock], view_type: str = 'daily') -> List[Dict[str, Any]]:
        all_entries = [
            entry for block in blocks for entry in block.usage_entries]
        if view_type == 'daily':
            return self.aggregate_daily(all_entries)
        elif view_type == 'monthly':
            return self.aggregate_monthly(all_entries)
        else:
            raise ValueError(
                "Unsupported view_type. Use 'daily' or 'monthly'.")

    def calculate_totals(self, aggregated_data: List[Dict[str, Any]]) -> Dict[str, Any]:
        total_value = sum(item['total'] for item in aggregated_data)
        return {'total': total_value}

    def aggregate(self, entries: List[UsageEntry], start_date: Optional[datetime] = None, end_date: Optional[datetime] = None) -> List[Dict[str, Any]]:
        if self.aggregation_mode == 'daily':
            return self.aggregate_daily(entries, start_date, end_date)
        elif self.aggregation_mode == 'monthly':
            return self.aggregate_monthly(entries, start_date, end_date)
        else:
            raise ValueError(
                "Unsupported aggregation_mode. Use 'daily' or 'monthly'.")
