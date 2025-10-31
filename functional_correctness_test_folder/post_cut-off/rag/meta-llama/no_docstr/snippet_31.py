
from datetime import datetime
from typing import List, Dict, Any, Callable, Optional


class UsageEntry:
    def __init__(self, timestamp: datetime, data: Dict[str, Any]):
        self.timestamp = timestamp
        self.data = data


class SessionBlock:
    def __init__(self, entries: List[UsageEntry]):
        self.entries = entries


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
        aggregated_data = {}
        for entry in entries:
            if start_date and entry.timestamp < start_date:
                continue
            if end_date and entry.timestamp > end_date:
                continue
            period_key = period_key_func(entry.timestamp)
            if period_key not in aggregated_data:
                aggregated_data[period_key] = {
                    'period': period_key, 'total': 0}
            aggregated_data[period_key]['total'] += entry.data.get('value', 0)
        return list(aggregated_data.values())

    def aggregate_daily(self, entries: List[UsageEntry], start_date: Optional[datetime] = None, end_date: Optional[datetime] = None) -> List[Dict[str, Any]]:
        """Aggregate usage data by day.

        Args:
            entries: List of usage entries
            start_date: Optional start date filter
            end_date: Optional end date filter

        Returns:
            List of daily aggregated data
        """
        def period_key_func(timestamp: datetime) -> str:
            return timestamp.strftime('%Y-%m-%d')
        return self._aggregate_by_period(entries, period_key_func, 'date', start_date, end_date)

    def aggregate_monthly(self, entries: List[UsageEntry], start_date: Optional[datetime] = None, end_date: Optional[datetime] = None) -> List[Dict[str, Any]]:
        """Aggregate usage data by month.

        Args:
            entries: List of usage entries
            start_date: Optional start date filter
            end_date: Optional end date filter

        Returns:
            List of monthly aggregated data
        """
        def period_key_func(timestamp: datetime) -> str:
            return timestamp.strftime('%Y-%m')
        return self._aggregate_by_period(entries, period_key_func, 'month', start_date, end_date)

    def aggregate_from_blocks(self, blocks: List[SessionBlock], view_type: str = 'daily') -> List[Dict[str, Any]]:
        """Aggregate data from session blocks.

        Args:
            blocks: List of session blocks
            view_type: Type of aggregation ('daily' or 'monthly')

        Returns:
            List of aggregated data
        """
        entries = [entry for block in blocks for entry in block.entries]
        if view_type == 'daily':
            return self.aggregate_daily(entries)
        elif view_type == 'monthly':
            return self.aggregate_monthly(entries)
        else:
            raise ValueError('Invalid view type')

    def calculate_totals(self, aggregated_data: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Calculate totals from aggregated data.

        Args:
            aggregated_data: List of aggregated daily or monthly data

        Returns:
            Dictionary with total statistics
        """
        total = sum(item['total'] for item in aggregated_data)
        return {'total': total}

    def aggregate(self, entries: List[UsageEntry], start_date: Optional[datetime] = None, end_date: Optional[datetime] = None) -> List[Dict[str, Any]]:
        """Main aggregation method that reads data and returns aggregated results.

        Returns:
            List of aggregated data based on aggregation_mode
        """
        if self.aggregation_mode == 'daily':
            return self.aggregate_daily(entries, start_date, end_date)
        elif self.aggregation_mode == 'monthly':
            return self.aggregate_monthly(entries, start_date, end_date)
        else:
            raise ValueError('Invalid aggregation mode')
