
import os
from typing import List, Dict, Any, Callable, Optional
from datetime import datetime, timezone
from collections import defaultdict

# Assume UsageEntry and SessionBlock are defined elsewhere and imported
# UsageEntry: has at least .timestamp (datetime), .user_id, .usage_amount, .session_id, etc.
# SessionBlock: has at least .entries (List[UsageEntry])


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

    def _aggregate_by_period(
        self,
        entries: List["UsageEntry"],
        period_key_func: Callable[[datetime], str],
        period_type: str,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None
    ) -> List[Dict[str, Any]]:
        '''Generic aggregation by time period.'''
        # Filter by date range if provided
        filtered = []
        for entry in entries:
            ts = entry.timestamp
            if start_date and ts < start_date:
                continue
            if end_date and ts > end_date:
                continue
            filtered.append(entry)

        # Group by period key
        period_groups = defaultdict(list)
        for entry in filtered:
            key = period_key_func(entry.timestamp)
            period_groups[key].append(entry)

        # Aggregate per period
        result = []
        for period, group in sorted(period_groups.items()):
            total_usage = sum(getattr(e, 'usage_amount', 0) for e in group)
            user_ids = set(getattr(e, 'user_id', None) for e in group)
            session_ids = set(getattr(e, 'session_id', None) for e in group)
            result.append({
                period_type: period,
                'total_usage': total_usage,
                'unique_users': len(user_ids - {None}),
                'unique_sessions': len(session_ids - {None}),
                'entry_count': len(group),
            })
        return result

    def aggregate_daily(
        self,
        entries: List["UsageEntry"],
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None
    ) -> List[Dict[str, Any]]:
        '''Aggregate usage data by day.'''
        def day_key(dt: datetime) -> str:
            return dt.astimezone(timezone.utc).strftime('%Y-%m-%d')
        return self._aggregate_by_period(entries, day_key, 'date', start_date, end_date)

    def aggregate_monthly(
        self,
        entries: List["UsageEntry"],
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None
    ) -> List[Dict[str, Any]]:
        '''Aggregate usage data by month.'''
        def month_key(dt: datetime) -> str:
            return dt.astimezone(timezone.utc).strftime('%Y-%m')
        return self._aggregate_by_period(entries, month_key, 'month', start_date, end_date)

    def aggregate_from_blocks(
        self,
        blocks: List["SessionBlock"],
        view_type: str = 'daily'
    ) -> List[Dict[str, Any]]:
        '''Aggregate data from session blocks.'''
        all_entries = []
        for block in blocks:
            all_entries.extend(getattr(block, 'entries', []))
        if view_type == 'daily':
            return self.aggregate_daily(all_entries)
        elif view_type == 'monthly':
            return self.aggregate_monthly(all_entries)
        else:
            raise ValueError(f"Unknown view_type: {view_type}")

    def calculate_totals(self, aggregated_data: List[Dict[str, Any]]) -> Dict[str, Any]:
        '''Calculate totals from aggregated data.'''
        total_usage = sum(d.get('total_usage', 0) for d in aggregated_data)
        total_entries = sum(d.get('entry_count', 0) for d in aggregated_data)
        total_unique_users = set()
        total_unique_sessions = set()
        for d in aggregated_data:
            # If you want to count unique users/sessions across all periods, you need to store them
            # But since only counts are available, we sum the counts (may overcount if users appear in multiple periods)
            pass
        # For unique users/sessions across all periods, you need to pass the original entries, not just the aggregates.
        return {
            'total_usage': total_usage,
            'total_entries': total_entries,
            'periods': len(aggregated_data),
        }

    def aggregate_main(
        self,
        entries: List["UsageEntry"],
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None
    ) -> List[Dict[str, Any]]:
        '''Main aggregation method that reads data and returns aggregated results.'''
        if self.aggregation_mode == 'daily':
            return self.aggregate_daily(entries, start_date, end_date)
        elif self.aggregation_mode == 'monthly':
            return self.aggregate_monthly(entries, start_date, end_date)
        else:
            raise ValueError(
                f"Unknown aggregation_mode: {self.aggregation_mode}")
