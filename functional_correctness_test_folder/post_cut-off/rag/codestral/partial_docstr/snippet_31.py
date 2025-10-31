
from datetime import datetime
from typing import List, Dict, Any, Callable, Optional
from collections import defaultdict


class UsageEntry:
    def __init__(self, timestamp: datetime, duration: float, user_id: str):
        self.timestamp = timestamp
        self.duration = duration
        self.user_id = user_id


class SessionBlock:
    def __init__(self, start_time: datetime, end_time: datetime, user_id: str):
        self.start_time = start_time
        self.end_time = end_time
        self.user_id = user_id


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
        aggregated = defaultdict(
            lambda: {'count': 0, 'total_duration': 0.0, 'users': set()})

        for entry in entries:
            if start_date and entry.timestamp < start_date:
                continue
            if end_date and entry.timestamp > end_date:
                continue

            period_key = period_key_func(entry.timestamp)
            aggregated[period_key]['count'] += 1
            aggregated[period_key]['total_duration'] += entry.duration
            aggregated[period_key]['users'].add(entry.user_id)

        result = []
        for period_key, data in aggregated.items():
            result.append({
                period_type: period_key,
                'count': data['count'],
                'total_duration': data['total_duration'],
                'unique_users': len(data['users'])
            })

        return sorted(result, key=lambda x: x[period_type])

    def aggregate_daily(self, entries: List[UsageEntry], start_date: Optional[datetime] = None, end_date: Optional[datetime] = None) -> List[Dict[str, Any]]:
        '''Aggregate usage data by day.
        Args:
            entries: List of usage entries
            start_date: Optional start date filter
            end_date: Optional end date filter
        Returns:
            List of daily aggregated data
        '''
        def get_date_key(timestamp: datetime) -> str:
            return timestamp.strftime('%Y-%m-%d')

        return self._aggregate_by_period(entries, get_date_key, 'date', start_date, end_date)

    def aggregate_monthly(self, entries: List[UsageEntry], start_date: Optional[datetime] = None, end_date: Optional[datetime] = None) -> List[Dict[str, Any]]:
        '''Aggregate usage data by month.
        Args:
            entries: List of usage entries
            start_date: Optional start date filter
            end_date: Optional end date filter
        Returns:
            List of monthly aggregated data
        '''
        def get_month_key(timestamp: datetime) -> str:
            return timestamp.strftime('%Y-%m')

        return self._aggregate_by_period(entries, get_month_key, 'month', start_date, end_date)

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
            entries.append(UsageEntry(
                timestamp=block.start_time,
                duration=(block.end_time - block.start_time).total_seconds(),
                user_id=block.user_id
            ))

        if view_type == 'daily':
            return self.aggregate_daily(entries)
        elif view_type == 'monthly':
            return self.aggregate_monthly(entries)
        else:
            raise ValueError(
                f"Invalid view_type: {view_type}. Must be 'daily' or 'monthly'")

    def calculate_totals(self, aggregated_data: List[Dict[str, Any]]) -> Dict[str, Any]:
        '''Calculate totals from aggregated data.
        Args:
            aggregated_data: List of aggregated daily or monthly data
        Returns:
            Dictionary with total statistics
        '''
        total_count = sum(item['count'] for item in aggregated_data)
        total_duration = sum(item['total_duration']
                             for item in aggregated_data)
        unique_users = set()
        for item in aggregated_data:
            unique_users.update(item.get('users', set()))

        return {
            'total_count': total_count,
            'total_duration': total_duration,
            'unique_users': len(unique_users)
        }

    def aggregate(self) -> List[Dict[str, Any]]:
        '''Main aggregation method that reads data and returns aggregated results.
        Returns:
            List of aggregated data based on aggregation_mode
        '''
        # In a real implementation, this would read data from self.data_path
        # For this example, we'll assume we have some sample data
        sample_entries = [
            UsageEntry(datetime(2023, 1, 1, 10, 0), 3600, "user1"),
            UsageEntry(datetime(2023, 1, 1, 12, 0), 1800, "user2"),
            UsageEntry(datetime(2023, 1, 2, 9, 0), 2700, "user1"),
            UsageEntry(datetime(2023, 2, 1, 8, 0), 3600, "user3"),
            UsageEntry(datetime(2023, 2, 15, 14, 0), 1800, "user2"),
        ]

        if self.aggregation_mode == 'daily':
            return self.aggregate_daily(sample_entries)
        elif self.aggregation_mode == 'monthly':
            return self.aggregate_monthly(sample_entries)
        else:
            raise ValueError(
                f"Invalid aggregation_mode: {self.aggregation_mode}. Must be 'daily' or 'monthly'")
