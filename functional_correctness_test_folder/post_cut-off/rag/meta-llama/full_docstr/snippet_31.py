
from typing import List, Dict, Any, Callable, Optional
from datetime import datetime
import pytz
from collections import defaultdict


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
        self.timezone = pytz.timezone(timezone)

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
        aggregated_data = defaultdict(lambda: defaultdict(int))
        for entry in entries:
            timestamp = entry.timestamp.astimezone(self.timezone)
            if (start_date is None or timestamp >= start_date) and (end_date is None or timestamp <= end_date):
                period_key = period_key_func(timestamp)
                for key, value in entry.data.items():
                    aggregated_data[period_key][key] += value

        result = []
        for period_key, data in aggregated_data.items():
            data['period'] = period_key
            data['period_type'] = period_type
            result.append(dict(data))
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
        return self._aggregate_by_period(entries, lambda dt: dt.strftime('%Y-%m-%d'), 'date', start_date, end_date)

    def aggregate_monthly(self, entries: List[UsageEntry], start_date: Optional[datetime] = None, end_date: Optional[datetime] = None) -> List[Dict[str, Any]]:
        """Aggregate usage data by month.

        Args:
            entries: List of usage entries
            start_date: Optional start date filter
            end_date: Optional end date filter

        Returns:
            List of monthly aggregated data
        """
        return self._aggregate_by_period(entries, lambda dt: dt.strftime('%Y-%m'), 'month', start_date, end_date)

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
            raise ValueError(
                "Invalid view_type. Must be 'daily' or 'monthly'.")

    def calculate_totals(self, aggregated_data: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Calculate totals from aggregated data.

        Args:
            aggregated_data: List of aggregated daily or monthly data

        Returns:
            Dictionary with total statistics
        """
        totals = defaultdict(int)
        for data in aggregated_data:
            for key, value in data.items():
                if key not in ['period', 'period_type']:
                    totals[key] += value
        return dict(totals)

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
            raise ValueError(
                "Invalid aggregation_mode. Must be 'daily' or 'monthly'.")
