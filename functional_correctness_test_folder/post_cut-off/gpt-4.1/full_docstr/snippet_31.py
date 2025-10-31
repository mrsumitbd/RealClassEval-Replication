
import os
from typing import List, Dict, Any, Callable, Optional
from datetime import datetime, timedelta
import pytz

# Dummy UsageEntry and SessionBlock for type hinting


class UsageEntry:
    def __init__(self, timestamp: datetime, usage: float):
        self.timestamp = timestamp
        self.usage = usage


class SessionBlock:
    def __init__(self, entries: List[UsageEntry]):
        self.entries = entries


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
        # Filter by date range if provided
        filtered_entries = []
        for entry in entries:
            ts = entry.timestamp.astimezone(self.timezone)
            if start_date and ts < start_date.astimezone(self.timezone):
                continue
            if end_date and ts > end_date.astimezone(self.timezone):
                continue
            filtered_entries.append(entry)

        # Aggregate by period
        period_data = {}
        for entry in filtered_entries:
            ts = entry.timestamp.astimezone(self.timezone)
            key = period_key_func(ts)
            if key not in period_data:
                period_data[key] = {
                    period_type: key,
                    'total_usage': 0.0,
                    'entry_count': 0,
                }
            period_data[key]['total_usage'] += entry.usage
            period_data[key]['entry_count'] += 1

        # Sort by period key
        sorted_keys = sorted(period_data.keys())
        return [period_data[k] for k in sorted_keys]

    def aggregate_daily(self, entries: List[UsageEntry], start_date: Optional[datetime] = None, end_date: Optional[datetime] = None) -> List[Dict[str, Any]]:
        '''Aggregate usage data by day.
        Args:
            entries: List of usage entries
            start_date: Optional start date filter
            end_date: Optional end date filter
        Returns:
            List of daily aggregated data
        '''
        def day_key(dt: datetime) -> str:
            return dt.strftime('%Y-%m-%d')
        return self._aggregate_by_period(entries, day_key, 'date', start_date, end_date)

    def aggregate_monthly(self, entries: List[UsageEntry], start_date: Optional[datetime] = None, end_date: Optional[datetime] = None) -> List[Dict[str, Any]]:
        '''Aggregate usage data by month.
        Args:
            entries: List of usage entries
            start_date: Optional start date filter
            end_date: Optional end date filter
        Returns:
            List of monthly aggregated data
        '''
        def month_key(dt: datetime) -> str:
            return dt.strftime('%Y-%m')
        return self._aggregate_by_period(entries, month_key, 'month', start_date, end_date)

    def aggregate_from_blocks(self, blocks: List[SessionBlock], view_type: str = 'daily') -> List[Dict[str, Any]]:
        '''Aggregate data from session blocks.
        Args:
            blocks: List of session blocks
            view_type: Type of aggregation ('daily' or 'monthly')
        Returns:
            List of aggregated data
        '''
        all_entries = []
        for block in blocks:
            all_entries.extend(block.entries)
        if view_type == 'monthly':
            return self.aggregate_monthly(all_entries)
        else:
            return self.aggregate_daily(all_entries)

    def calculate_totals(self, aggregated_data: List[Dict[str, Any]]) -> Dict[str, Any]:
        '''Calculate totals from aggregated data.
        Args:
            aggregated_data: List of aggregated daily or monthly data
        Returns:
            Dictionary with total statistics
        '''
        total_usage = sum(item['total_usage'] for item in aggregated_data)
        total_entries = sum(item['entry_count'] for item in aggregated_data)
        periods = len(aggregated_data)
        avg_usage = total_usage / periods if periods > 0 else 0.0
        return {
            'total_usage': total_usage,
            'total_entries': total_entries,
            'periods': periods,
            'average_usage_per_period': avg_usage
        }

    def aggregate(self, entries: List[UsageEntry], start_date: Optional[datetime] = None, end_date: Optional[datetime] = None) -> List[Dict[str, Any]]:
        '''Main aggregation method that reads data and returns aggregated results.
        Returns:
            List of aggregated data based on aggregation_mode
        '''
        if self.aggregation_mode == 'monthly':
            return self.aggregate_monthly(entries, start_date, end_date)
        else:
            return self.aggregate_daily(entries, start_date, end_date)
