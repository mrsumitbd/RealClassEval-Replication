
from datetime import datetime
from typing import List, Dict, Any, Callable, Optional
from collections import defaultdict


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
        period_data = defaultdict(lambda: {
            'count': 0,
            'duration': 0,
            'users': set(),
            'sessions': set()
        })

        for entry in entries:
            timestamp = entry.timestamp
            if start_date and timestamp < start_date:
                continue
            if end_date and timestamp > end_date:
                continue

            period_key = period_key_func(timestamp)
            period_data[period_key]['count'] += 1
            period_data[period_key]['duration'] += entry.duration
            period_data[period_key]['users'].add(entry.user_id)
            period_data[period_key]['sessions'].add(entry.session_id)

        result = []
        for period_key, data in sorted(period_data.items()):
            result.append({
                'period': period_key,
                'period_type': period_type,
                'count': data['count'],
                'duration': data['duration'],
                'unique_users': len(data['users']),
                'unique_sessions': len(data['sessions'])
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
        def day_key(timestamp: datetime) -> str:
            return timestamp.strftime('%Y-%m-%d')

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
        def month_key(timestamp: datetime) -> str:
            return timestamp.strftime('%Y-%m')

        return self._aggregate_by_period(entries, month_key, 'month', start_date, end_date)

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
            entries.extend(block.usage_entries)

        if view_type == 'daily':
            return self.aggregate_daily(entries)
        else:
            return self.aggregate_monthly(entries)

    def calculate_totals(self, aggregated_data: List[Dict[str, Any]]) -> Dict[str, Any]:
        '''Calculate totals from aggregated data.
        Args:
            aggregated_data: List of aggregated daily or monthly data
        Returns:
            Dictionary with total statistics
        '''
        totals = {
            'total_count': 0,
            'total_duration': 0,
            'total_unique_users': 0,
            'total_unique_sessions': 0,
            'user_set': set(),
            'session_set': set()
        }

        for data in aggregated_data:
            totals['total_count'] += data['count']
            totals['total_duration'] += data['duration']
            totals['user_set'].update(data.get('users', set()))
            totals['session_set'].update(data.get('sessions', set()))

        totals['total_unique_users'] = len(totals['user_set'])
        totals['total_unique_sessions'] = len(totals['session_set'])

        return totals

    def aggregate(self) -> List[Dict[str, Any]]:
        '''Main aggregation method that reads data and returns aggregated results.
        Returns:
            List of aggregated data based on aggregation_mode
        '''
        # Implementation would read data from self.data_path
        # and call appropriate aggregation method
        entries = []  # Would be populated from data source
        if self.aggregation_mode == 'daily':
            return self.aggregate_daily(entries)
        else:
            return self.aggregate_monthly(entries)
