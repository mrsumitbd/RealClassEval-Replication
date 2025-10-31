
from typing import List, Dict, Any, Callable, Optional
from datetime import datetime, timedelta
import pytz


class UsageEntry:
    def __init__(self, timestamp: datetime, usage: float):
        self.timestamp = timestamp
        self.usage = usage


class SessionBlock:
    def __init__(self, start_time: datetime, end_time: datetime, usage_entries: List[UsageEntry]):
        self.start_time = start_time
        self.end_time = end_time
        self.usage_entries = usage_entries


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
        self.timezone = timezone
        self.tz = pytz.timezone(timezone)

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
        if start_date:
            start_date = start_date.astimezone(self.tz)
        if end_date:
            end_date = end_date.astimezone(self.tz)

        aggregated_data = {}
        for entry in entries:
            ts = entry.timestamp.astimezone(self.tz)
            if start_date and ts < start_date:
                continue
            if end_date and ts > end_date:
                continue
            key = period_key_func(ts)
            if key not in aggregated_data:
                aggregated_data[key] = {'period': key,
                                        'total_usage': 0.0, 'count': 0}
            aggregated_data[key]['total_usage'] += entry.usage
            aggregated_data[key]['count'] += 1

        return list(aggregated_data.values())

    def aggregate_daily(self, entries: List[UsageEntry], start_date: Optional[datetime] = None, end_date: Optional[datetime] = None) -> List[Dict[str, Any]]:
        '''Aggregate usage data by day.
        Args:
            entries: List of usage entries
            start_date: Optional start date filter
            end_date: Optional end date filter
        Returns:
            List of daily aggregated data
        '''
        return self._aggregate_by_period(entries, lambda ts: ts.strftime('%Y-%m-%d'), 'date', start_date, end_date)

    def aggregate_monthly(self, entries: List[UsageEntry], start_date: Optional[datetime] = None, end_date: Optional[datetime] = None) -> List[Dict[str, Any]]:
        '''Aggregate usage data by month.
        Args:
            entries: List of usage entries
            start_date: Optional start date filter
            end_date: Optional end date filter
        Returns:
            List of monthly aggregated data
        '''
        return self._aggregate_by_period(entries, lambda ts: ts.strftime('%Y-%m'), 'month', start_date, end_date)

    def aggregate_from_blocks(self, blocks: List[SessionBlock], view_type: str = 'daily') -> List[Dict[str, Any]]:
        '''Aggregate data from session blocks.
        Args:
            blocks: List of session blocks
            view_type: Type of aggregation ('daily' or 'monthly')
        Returns:
            List of aggregated data
        '''
        all_entries = [
            entry for block in blocks for entry in block.usage_entries]
        if view_type == 'daily':
            return self.aggregate_daily(all_entries)
        elif view_type == 'monthly':
            return self.aggregate_monthly(all_entries)
        else:
            raise ValueError("view_type must be 'daily' or 'monthly'")

    def calculate_totals(self, aggregated_data: List[Dict[str, Any]]) -> Dict[str, Any]:
        '''Calculate totals from aggregated data.
        Args:
            aggregated_data: List of aggregated daily or monthly data
        Returns:
            Dictionary with total statistics
        '''
        total_usage = sum(item['total_usage'] for item in aggregated_data)
        total_count = sum(item['count'] for item in aggregated_data)
        return {'total_usage': total_usage, 'total_count': total_count}

    def aggregate(self, start_date: Optional[datetime] = None, end_date: Optional[datetime] = None) -> List[Dict[str, Any]]:
        '''Main aggregation method that reads data and returns aggregated results.
        Returns:
            List of aggregated data based on aggregation_mode
        '''
        # This method would typically read data from self.data_path
        # For the sake of this example, we'll assume entries are already loaded
        entries = self._load_entries_from_path(self.data_path)
        if self.aggregation_mode == 'daily':
            return self.aggregate_daily(entries, start_date, end_date)
        elif self.aggregation_mode == 'monthly':
            return self.aggregate_monthly(entries, start_date, end_date)
        else:
            raise ValueError("aggregation_mode must be 'daily' or 'monthly'")

    def _load_entries_from_path(self, path: str) -> List[UsageEntry]:
        # Placeholder for loading entries from a file or database
        # This should be implemented based on the actual data source
        return []
