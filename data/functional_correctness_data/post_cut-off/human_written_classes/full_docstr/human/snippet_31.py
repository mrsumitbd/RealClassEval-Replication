from typing import Any, Callable, Dict, List, Optional
from claude_monitor.utils.time_utils import TimezoneHandler
from datetime import datetime
from claude_monitor.core.models import SessionBlock, UsageEntry, normalize_model_name

class UsageAggregator:
    """Aggregates usage data for daily and monthly reports."""

    def __init__(self, data_path: str, aggregation_mode: str='daily', timezone: str='UTC'):
        """Initialize the aggregator.

        Args:
            data_path: Path to the data directory
            aggregation_mode: Mode of aggregation ('daily' or 'monthly')
            timezone: Timezone string for date formatting
        """
        self.data_path = data_path
        self.aggregation_mode = aggregation_mode
        self.timezone = timezone
        self.timezone_handler = TimezoneHandler()

    def _aggregate_by_period(self, entries: List[UsageEntry], period_key_func: Callable[[datetime], str], period_type: str, start_date: Optional[datetime]=None, end_date: Optional[datetime]=None) -> List[Dict[str, Any]]:
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
        period_data: Dict[str, AggregatedPeriod] = {}
        for entry in entries:
            if start_date and entry.timestamp < start_date:
                continue
            if end_date and entry.timestamp > end_date:
                continue
            period_key = period_key_func(entry.timestamp)
            if period_key not in period_data:
                period_data[period_key] = AggregatedPeriod(period_key)
            period_data[period_key].add_entry(entry)
        result = []
        for period_key in sorted(period_data.keys()):
            period = period_data[period_key]
            result.append(period.to_dict(period_type))
        return result

    def aggregate_daily(self, entries: List[UsageEntry], start_date: Optional[datetime]=None, end_date: Optional[datetime]=None) -> List[Dict[str, Any]]:
        """Aggregate usage data by day.

        Args:
            entries: List of usage entries
            start_date: Optional start date filter
            end_date: Optional end date filter

        Returns:
            List of daily aggregated data
        """
        return self._aggregate_by_period(entries, lambda timestamp: timestamp.strftime('%Y-%m-%d'), 'date', start_date, end_date)

    def aggregate_monthly(self, entries: List[UsageEntry], start_date: Optional[datetime]=None, end_date: Optional[datetime]=None) -> List[Dict[str, Any]]:
        """Aggregate usage data by month.

        Args:
            entries: List of usage entries
            start_date: Optional start date filter
            end_date: Optional end date filter

        Returns:
            List of monthly aggregated data
        """
        return self._aggregate_by_period(entries, lambda timestamp: timestamp.strftime('%Y-%m'), 'month', start_date, end_date)

    def aggregate_from_blocks(self, blocks: List[SessionBlock], view_type: str='daily') -> List[Dict[str, Any]]:
        """Aggregate data from session blocks.

        Args:
            blocks: List of session blocks
            view_type: Type of aggregation ('daily' or 'monthly')

        Returns:
            List of aggregated data
        """
        if view_type not in ['daily', 'monthly']:
            raise ValueError(f"Invalid view type: {view_type}. Must be 'daily' or 'monthly'")
        all_entries = []
        for block in blocks:
            if not block.is_gap:
                all_entries.extend(block.entries)
        if view_type == 'daily':
            return self.aggregate_daily(all_entries)
        else:
            return self.aggregate_monthly(all_entries)

    def calculate_totals(self, aggregated_data: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Calculate totals from aggregated data.

        Args:
            aggregated_data: List of aggregated daily or monthly data

        Returns:
            Dictionary with total statistics
        """
        total_stats = AggregatedStats()
        for data in aggregated_data:
            total_stats.input_tokens += data.get('input_tokens', 0)
            total_stats.output_tokens += data.get('output_tokens', 0)
            total_stats.cache_creation_tokens += data.get('cache_creation_tokens', 0)
            total_stats.cache_read_tokens += data.get('cache_read_tokens', 0)
            total_stats.cost += data.get('total_cost', 0.0)
            total_stats.count += data.get('entries_count', 0)
        return {'input_tokens': total_stats.input_tokens, 'output_tokens': total_stats.output_tokens, 'cache_creation_tokens': total_stats.cache_creation_tokens, 'cache_read_tokens': total_stats.cache_read_tokens, 'total_tokens': total_stats.input_tokens + total_stats.output_tokens + total_stats.cache_creation_tokens + total_stats.cache_read_tokens, 'total_cost': total_stats.cost, 'entries_count': total_stats.count}

    def aggregate(self) -> List[Dict[str, Any]]:
        """Main aggregation method that reads data and returns aggregated results.

        Returns:
            List of aggregated data based on aggregation_mode
        """
        from claude_monitor.data.reader import load_usage_entries
        logger.info(f'Starting aggregation in {self.aggregation_mode} mode')
        entries, _ = load_usage_entries(data_path=self.data_path)
        if not entries:
            logger.warning('No usage entries found')
            return []
        for entry in entries:
            if entry.timestamp.tzinfo is None:
                entry.timestamp = self.timezone_handler.ensure_timezone(entry.timestamp)
        if self.aggregation_mode == 'daily':
            return self.aggregate_daily(entries)
        elif self.aggregation_mode == 'monthly':
            return self.aggregate_monthly(entries)
        else:
            raise ValueError(f'Invalid aggregation mode: {self.aggregation_mode}')