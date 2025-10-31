
from datetime import datetime
from typing import List, Dict, Any, Optional, Callable
from collections import defaultdict


class UsageEntry:
    '''Represents a single usage entry.'''

    def __init__(self, timestamp: datetime, value: float):
        self.timestamp = timestamp
        self.value = value


class SessionBlock:
    '''Represents a session block with start and end times.'''

    def __init__(self, start_time: datetime, end_time: datetime, value: float):
        self.start_time = start_time
        self.end_time = end_time
        self.value = value


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
        aggregated = defaultdict(float)
        count = defaultdict(int)

        for entry in entries:
            if start_date and entry.timestamp < start_date:
                continue
            if end_date and entry.timestamp > end_date:
                continue

            period_key = period_key_func(entry.timestamp)
            aggregated[period_key] += entry.value
            count[period_key] += 1

        result = []
        for period_key in sorted(aggregated.keys()):
            avg_value = aggregated[period_key] / \
                count[period_key] if count[period_key] > 0 else 0
            result.append({
                'period': period_key,
                'total': aggregated[period_key],
                'average': avg_value,
                'count': count[period_key]
            })

        return result

    def aggregate_daily(self, entries: List[UsageEntry], start_date: Optional[datetime] = None, end_date: Optional[datetime] = None) -> List[Dict[str, Any]]:
        '''Aggregate usage data by day.
        Args:
            entries: List of usage entries
            start_date: Optional start date filter
            end_date: Optional end date filter
        Returns:
            List of daily aggregated data
        '''
        def period_key_func(timestamp: datetime) -> str:
            return timestamp.strftime('%Y-%m-%d')

        return self._aggregate_by_period(entries, period_key_func, 'date', start_date, end_date)

    def aggregate_monthly(self, entries: List[UsageEntry], start_date: Optional[datetime] = None, end_date: Optional[datetime] = None) -> List[Dict[str, Any]]:
        '''Aggregate usage data by month.
        Args:
            entries: List of usage entries
            start_date: Optional start date filter
            end_date: Optional end date filter
        Returns:
            List of monthly aggregated data
        '''
        def period_key_func(timestamp: datetime) -> str:
            return timestamp.strftime('%Y-%m')

        return self._aggregate_by_period(entries, period_key_func, 'month', start_date, end_date)

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
            entries.append(UsageEntry(block.start_time, block.value))

        if view_type == 'daily':
            return self.aggregate_daily(entries)
        elif view_type == 'monthly':
            return self.aggregate_monthly(entries)
        else:
            raise ValueError(f"Invalid view type: {view_type}")

    def calculate_totals(self, aggregated_data: List[Dict[str, Any]]) -> Dict[str, Any]:
        '''Calculate totals from aggregated data.
        Args:
            aggregated_data: List of aggregated daily or monthly data
        Returns:
            Dictionary with total statistics
        '''
        total = sum(item['total'] for item in aggregated_data)
        count = sum(item['count'] for item in aggregated_data)
        average = total / count if count > 0 else 0

        return {
            'total': total,
            'average': average,
            'count': count
        }

    def aggregate(self, entries: List[UsageEntry], start_date: Optional[datetime] = None, end_date: Optional[datetime] = None) -> List[Dict[str, Any]]:
        '''Main aggregation method that reads data and returns aggregated results.
        Returns:
            List of aggregated data based on aggregation_mode
        '''
        if self.aggregation_mode == 'daily':
            return self.aggregate_daily(entries, start_date, end_date)
        elif self.aggregation_mode == 'monthly':
            return self.aggregate_monthly(entries, start_date, end_date)
        else:
            raise ValueError(
                f"Invalid aggregation mode: {self.aggregation_mode}")
