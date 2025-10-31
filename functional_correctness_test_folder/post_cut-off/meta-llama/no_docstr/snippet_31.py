
from typing import List, Callable, Dict, Any, Optional
from datetime import datetime
import pytz
from dataclasses import dataclass

# Assuming UsageEntry and SessionBlock are defined elsewhere


@dataclass
class UsageEntry:
    start_time: datetime
    end_time: datetime
    duration: int


@dataclass
class SessionBlock:
    start_time: datetime
    end_time: datetime
    usage_entries: List[UsageEntry]


class UsageAggregator:

    def __init__(self, data_path: str, aggregation_mode: str = 'daily', timezone: str = 'UTC'):
        self.data_path = data_path
        self.aggregation_mode = aggregation_mode
        self.timezone = pytz.timezone(timezone)

    def _aggregate_by_period(self, entries: List[UsageEntry], period_key_func: Callable[[datetime], str], period_type: str, start_date: Optional[datetime] = None, end_date: Optional[datetime] = None) -> List[Dict[str, Any]]:
        if start_date is None:
            start_date = min(entry.start_time.astimezone(
                self.timezone) for entry in entries)
        if end_date is None:
            end_date = max(entry.end_time.astimezone(self.timezone)
                           for entry in entries)

        aggregated_data = {}
        for entry in entries:
            entry_start_time = entry.start_time.astimezone(self.timezone)
            if start_date <= entry_start_time <= end_date:
                period_key = period_key_func(entry_start_time)
                if period_key not in aggregated_data:
                    aggregated_data[period_key] = {
                        'period': period_key, 'period_type': period_type, 'total_duration': 0}
                aggregated_data[period_key]['total_duration'] += entry.duration

        return list(aggregated_data.values())

    def aggregate_daily(self, entries: List[UsageEntry], start_date: Optional[datetime] = None, end_date: Optional[datetime] = None) -> List[Dict[str, Any]]:
        return self._aggregate_by_period(entries, lambda dt: dt.strftime('%Y-%m-%d'), 'daily', start_date, end_date)

    def aggregate_monthly(self, entries: List[UsageEntry], start_date: Optional[datetime] = None, end_date: Optional[datetime] = None) -> List[Dict[str, Any]]:
        return self._aggregate_by_period(entries, lambda dt: dt.strftime('%Y-%m'), 'monthly', start_date, end_date)

    def aggregate_from_blocks(self, blocks: List[SessionBlock], view_type: str = 'daily') -> List[Dict[str, Any]]:
        all_entries = [
            entry for block in blocks for entry in block.usage_entries]
        if view_type == 'daily':
            return self.aggregate_daily(all_entries)
        elif view_type == 'monthly':
            return self.aggregate_monthly(all_entries)
        else:
            raise ValueError('Invalid view type')

    def calculate_totals(self, aggregated_data: List[Dict[str, Any]]) -> Dict[str, Any]:
        total_duration = sum(item['total_duration']
                             for item in aggregated_data)
        return {'total_duration': total_duration}

    # Removed duplicate method definition
