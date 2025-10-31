
from typing import List, Callable, Optional, Dict, Any
from datetime import datetime
import pytz
from dataclasses import dataclass

# Assuming UsageEntry and SessionBlock are defined elsewhere


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
    '''Aggregates usage data for daily and monthly reports.'''

    def __init__(self, data_path: str, aggregation_mode: str = 'daily', timezone: str = 'UTC'):
        '''Initialize the aggregator.
        Args:
            data_path: Path to the data directory
            aggregation_mode: Mode of aggregation ('daily' or 'monthly')
            timezone: Timezone string for date formatting
        '''
        self.data_path = data_path
        self.aggregation_mode = aggregation_mode
        self.timezone = pytz.timezone(timezone)

    def _aggregate_by_period(self, entries: List[UsageEntry], period_key_func: Callable[[datetime], str], period_type: str, start_date: Optional[datetime] = None, end_date: Optional[datetime] = None) -> List[Dict[str, Any]]:
        '''Generic aggregation by time period.
        Args:
            entries: List of usage entries
            period_key_func: Function to extract period key from timestamp
            period_type: Type of period ('date' or 'month')
            start_date: Optional start date filter
            end_date: Optional end date filter
        Returns:
            List of aggregated data dictionaries
        '''
        filtered_entries = [entry for entry in entries
                            if (start_date is None or entry.timestamp >= start_date)
                            and (end_date is None or entry.timestamp <= end_date)]

        aggregated_data = {}
        for entry in filtered_entries:
            period_key = period_key_func(self._localize(entry.timestamp))
            if period_key not in aggregated_data:
                aggregated_data[period_key] = {
                    'period': period_key, 'total': 0, 'count': 0}
            aggregated_data[period_key]['total'] += entry.value
            aggregated_data[period_key]['count'] += 1

        return list(aggregated_data.values())

    def _localize(self, dt: datetime) -> datetime:
        if dt.tzinfo is None:
            return self.timezone.localize(dt)
        else:
            return dt.astimezone(self.timezone)

    def aggregate_daily(self, entries: List[UsageEntry], start_date: Optional[datetime] = None, end_date: Optional[datetime] = None) -> List[Dict[str, Any]]:
        '''Aggregate usage data by day.
        Args:
            entries: List of usage entries
            start_date: Optional start date filter
            end_date: Optional end date filter
        Returns:
            List of daily aggregated data
        '''
        return self._aggregate_by_period(entries, lambda dt: dt.strftime('%Y-%m-%d'), 'date', start_date, end_date)

    def aggregate_monthly(self, entries: List[UsageEntry], start_date: Optional[datetime] = None, end_date: Optional[datetime] = None) -> List[Dict[str, Any]]:
        '''Aggregate usage data by month.
        Args:
            entries: List of usage entries
            start_date: Optional start date filter
            end_date: Optional end date filter
        Returns:
            List of monthly aggregated data
        '''
        return self._aggregate_by_period(entries, lambda dt: dt.strftime('%Y-%m'), 'month', start_date, end_date)

    def aggregate_from_blocks(self, blocks: List[SessionBlock], view_type: str = 'daily') -> List[Dict[str, Any]]:
        '''Aggregate data from session blocks.
        Args:
            blocks: List of session blocks
            view_type: Type of aggregation ('daily' or 'monthly')
        Returns:
            List of aggregated data
        '''
        entries = []
        for block in blocks:
            # Assuming the value is constant over the block duration
            duration = (block.end_time -
                        block.start_time).total_seconds() / 3600  # in hours
            entries.append(UsageEntry(
                block.start_time, block.value * duration))

        if view_type == 'daily':
            return self.aggregate_daily(entries)
        elif view_type == 'monthly':
            return self.aggregate_monthly(entries)
        else:
            raise ValueError(
                "Invalid view_type. Must be 'daily' or 'monthly'.")

    def calculate_totals(self, aggregated_data: List[Dict[str, Any]]) -> Dict[str, Any]:
        '''Calculate totals from aggregated data.
        Args:
            aggregated_data: List of aggregated daily or monthly data
        Returns:
            Dictionary with total statistics
        '''
        total_value = sum(item['total'] for item in aggregated_data)
        total_count = sum(item['count'] for item in aggregated_data)
        return {'total_value': total_value, 'total_count': total_count, 'average': total_value / total_count if total_count > 0 else 0}

    def aggregate(self, entries: List[UsageEntry], start_date: Optional[datetime] = None, end_date: Optional[datetime] = None) -> List[Dict[str, Any]]:
        '''Main aggregation method that returns aggregated results based on aggregation_mode.
        Args:
            entries: List of usage entries
            start_date: Optional start date filter
            end_date: Optional end date filter
        Returns:
            List of aggregated data
        '''
        if self.aggregation_mode == 'daily':
            return self.aggregate_daily(entries, start_date, end_date)
        elif self.aggregation_mode == 'monthly':
            return self.aggregate_monthly(entries, start_date, end_date)
        else:
            raise ValueError(
                "Invalid aggregation_mode. Must be 'daily' or 'monthly'.")
