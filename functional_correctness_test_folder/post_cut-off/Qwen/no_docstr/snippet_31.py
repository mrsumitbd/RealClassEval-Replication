
from typing import List, Dict, Any, Callable, Optional
from datetime import datetime, timedelta, timezone as tz
from collections import defaultdict


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
        self.timezone = tz(timedelta(hours=int(timezone[:3]), minutes=int(
            timezone[3:]))) if timezone else tz.utc

    def _aggregate_by_period(self, entries: List[UsageEntry], period_key_func: Callable[[datetime], str], period_type: str, start_date: Optional[datetime] = None, end_date: Optional[datetime] = None) -> List[Dict[str, Any]]:
        aggregated_data = defaultdict(float)
        for entry in entries:
            if (start_date is None or entry.timestamp >= start_date) and (end_date is None or entry.timestamp <= end_date):
                period_key = period_key_func(entry.timestamp)
                aggregated_data[period_key] += entry.value
        return [{'period': key, period_type: key, 'total': value} for key, value in aggregated_data.items()]

    def aggregate_daily(self, entries: List[UsageEntry], start_date: Optional[datetime] = None, end_date: Optional[datetime] = None) -> List[Dict[str, Any]]:
        return self._aggregate_by_period(entries, lambda x: x.astimezone(self.timezone).strftime('%Y-%m-%d'), 'date', start_date, end_date)

    def aggregate_monthly(self, entries: List[UsageEntry], start_date: Optional[datetime] = None, end_date: Optional[datetime] = None) -> List[Dict[str, Any]]:
        return self._aggregate_by_period(entries, lambda x: x.astimezone(self.timezone).strftime('%Y-%m'), 'month', start_date, end_date)

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
