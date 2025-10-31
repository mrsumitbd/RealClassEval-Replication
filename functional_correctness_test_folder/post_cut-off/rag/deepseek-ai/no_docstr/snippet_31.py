
from datetime import datetime
from typing import List, Dict, Any, Callable, Optional
from collections import defaultdict


class UsageAggregator:
    """Aggregates usage data for daily and monthly reports."""

    def __init__(self, data_path: str, aggregation_mode: str = 'daily', timezone: str = 'UTC'):
        """Initialize the aggregator.
        Args:
            data_path: Path to the data directory
            aggregation_mode: Mode of aggregation ('daily' or 'monthly')
            timezone: Timezone string for date formatting
        """
        self.data_path = data_path
        self.aggregation_mode = aggregation_mode
        self.timezone = timezone

    def _aggregate_by_period(self, entries: List[UsageEntry], period_key_func: Callable[[datetime], str], period_type: str, start_date: Optional[datetime] = None, end_date: Optional[datetime] = None) -> List[Dict[str, Any]]:
        """Generic aggregation by time period.
        Args:
            entries: List of usage entries
            period_key_func: Function to extract period key from timestamp
            period_type: Type of period ('date' or 'month')
            start_date: Optional start date filter
            end_date: Optional end date filter
        Returns:
            List of aggregated data dictionaries
        """
        period_data = defaultdict(lambda: {
            'total_usage': 0,
            'total_sessions': 0,
            'unique_users': set(),
            'period_type': period_type
        })

        for entry in entries:
            if start_date and entry.timestamp < start_date:
                continue
            if end_date and entry.timestamp > end_date:
                continue

            period_key = period_key_func(entry.timestamp)
            period_data[period_key]['total_usage'] += entry.usage_amount
            period_data[period_key]['total_sessions'] += 1
            period_data[period_key]['unique_users'].add(entry.user_id)
            period_data[period_key]['period'] = period_key

        result = []
        for period_key, data in period_data.items():
            result.append({
                'period': period_key,
                'total_usage': data['total_usage'],
                'total_sessions': data['total_sessions'],
                'unique_users': len(data['unique_users']),
                'period_type': period_type
            })

        return sorted(result, key=lambda x: x['period'])

    def aggregate_daily(self, entries: List[UsageEntry], start_date: Optional[datetime] = None, end_date: Optional[datetime] = None) -> List[Dict[str, Any]]:
        """Aggregate usage data by day.
        Args:
            entries: List of usage entries
            start_date: Optional start date filter
            end_date: Optional end date filter
        Returns:
            List of daily aggregated data
        """
        def day_key_func(timestamp: datetime) -> str:
            return timestamp.strftime('%Y-%m-%d')

        return self._aggregate_by_period(
            entries,
            day_key_func,
            'date',
            start_date,
            end_date
        )

    def aggregate_monthly(self, entries: List[UsageEntry], start_date: Optional[datetime] = None, end_date: Optional[datetime] = None) -> List[Dict[str, Any]]:
        """Aggregate usage data by month.
        Args:
            entries: List of usage entries
            start_date: Optional start date filter
            end_date: Optional end date filter
        Returns:
            List of monthly aggregated data
        """
        def month_key_func(timestamp: datetime) -> str:
            return timestamp.strftime('%Y-%m')

        return self._aggregate_by_period(
            entries,
            month_key_func,
            'month',
            start_date,
            end_date
        )

    def aggregate_from_blocks(self, blocks: List[SessionBlock], view_type: str = 'daily') -> List[Dict[str, Any]]:
        """Aggregate data from session blocks.
        Args:
            blocks: List of session blocks
            view_type: Type of aggregation ('daily' or 'monthly')
        Returns:
            List of aggregated data
        """
        entries = []
        for block in blocks:
            entries.append(UsageEntry(
                user_id=block.user_id,
                timestamp=block.start_time,
                usage_amount=block.usage_amount
            ))

        if view_type == 'daily':
            return self.aggregate_daily(entries)
        else:
            return self.aggregate_monthly(entries)

    def calculate_totals(self, aggregated_data: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Calculate totals from aggregated data.
        Args:
            aggregated_data: List of aggregated daily or monthly data
        Returns:
            Dictionary with total statistics
        """
        totals = {
            'total_usage': 0,
            'total_sessions': 0,
            'unique_users': set(),
            'period_count': len(aggregated_data)
        }

        for period_data in aggregated_data:
            totals['total_usage'] += period_data['total_usage']
            totals['total_sessions'] += period_data['total_sessions']
            totals['unique_users'].update(set([period_data['period']]))

        totals['unique_users'] = len(totals['unique_users'])
        return totals

    def aggregate(self) -> List[Dict[str, Any]]:
        """Main aggregation method that reads data and returns aggregated results.
        Returns:
            List of aggregated data based on aggregation_mode
        """
        entries = self._load_entries()

        if self.aggregation_mode == 'daily':
            return self.aggregate_daily(entries)
        else:
            return self.aggregate_monthly(entries)
