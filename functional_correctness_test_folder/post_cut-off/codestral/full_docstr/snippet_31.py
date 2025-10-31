
from typing import List, Dict, Any, Callable, Optional
from datetime import datetime
import pytz
import os
import json


class UsageEntry:
    def __init__(self, timestamp: datetime, value: float):
        self.timestamp = timestamp
        self.value = value


class SessionBlock:
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
        aggregated_data = {}
        for entry in entries:
            if start_date and entry.timestamp < start_date:
                continue
            if end_date and entry.timestamp > end_date:
                continue
            period_key = period_key_func(entry.timestamp)
            if period_key not in aggregated_data:
                aggregated_data[period_key] = {'total': 0, 'count': 0}
            aggregated_data[period_key]['total'] += entry.value
            aggregated_data[period_key]['count'] += 1

        result = []
        for period_key, data in aggregated_data.items():
            if period_type == 'date':
                period_date = datetime.strptime(period_key, '%Y-%m-%d').date()
            else:
                period_date = datetime.strptime(period_key, '%Y-%m').date()
            result.append({
                'period': period_key,
                'total': data['total'],
                'average': data['total'] / data['count'],
                'count': data['count']
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
        def get_date_key(timestamp: datetime) -> str:
            return timestamp.astimezone(self.timezone).strftime('%Y-%m-%d')

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
            return timestamp.astimezone(self.timezone).strftime('%Y-%m')

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
            entries.append(UsageEntry(block.start_time, block.value))
            entries.append(UsageEntry(block.end_time, -block.value))

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
        total = sum(item['total'] for item in aggregated_data)
        count = sum(item['count'] for item in aggregated_data)
        return {
            'total': total,
            'average': total / count if count > 0 else 0,
            'count': count
        }

    def aggregate(self) -> List[Dict[str, Any]]:
        '''Main aggregation method that reads data and returns aggregated results.
        Returns:
            List of aggregated data based on aggregation_mode
        '''
        entries = []
        for filename in os.listdir(self.data_path):
            if filename.endswith('.json'):
                with open(os.path.join(self.data_path, filename), 'r') as f:
                    data = json.load(f)
                    for item in data:
                        timestamp = datetime.strptime(
                            item['timestamp'], '%Y-%m-%d %H:%M:%S')
                        entries.append(UsageEntry(timestamp, item['value']))

        if self.aggregation_mode == 'daily':
            return self.aggregate_daily(entries)
        else:
            return self.aggregate_monthly(entries)
