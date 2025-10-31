
import os
from typing import List, Dict, Any, Callable, Optional
from datetime import datetime
from collections import defaultdict
import pytz

# Assume UsageEntry and SessionBlock are defined elsewhere and imported
# For this implementation, we assume UsageEntry has at least:
#   - timestamp: datetime
#   - user_id: str
#   - usage: float (or int)
#   - (possibly other fields)
# And SessionBlock has:
#   - entries: List[UsageEntry]


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

    def _aggregate_by_period(
        self,
        entries: List['UsageEntry'],
        period_key_func: Callable[[datetime], str],
        period_type: str,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None
    ) -> List[Dict[str, Any]]:
        '''Generic aggregation by time period.'''
        # Filter by date if needed
        filtered = []
        for entry in entries:
            ts = entry.timestamp
            if ts.tzinfo is None:
                ts = self.timezone.localize(ts)
            else:
                ts = ts.astimezone(self.timezone)
            if start_date:
                if start_date.tzinfo is None:
                    start = self.timezone.localize(start_date)
                else:
                    start = start_date.astimezone(self.timezone)
                if ts < start:
                    continue
            if end_date:
                if end_date.tzinfo is None:
                    end = self.timezone.localize(end_date)
                else:
                    end = end_date.astimezone(self.timezone)
                if ts > end:
                    continue
            filtered.append((entry, ts))

        # Aggregate by period key
        period_data = defaultdict(list)
        for entry, ts in filtered:
            key = period_key_func(ts)
            period_data[key].append(entry)

        # For each period, aggregate stats
        result = []
        for period_key, period_entries in sorted(period_data.items()):
            total_usage = sum(getattr(e, 'usage', 0) for e in period_entries)
            user_ids = set(getattr(e, 'user_id', None) for e in period_entries)
            result.append({
                period_type: period_key,
                'total_usage': total_usage,
                'unique_users': len(user_ids),
                'entry_count': len(period_entries),
            })
        return result

    def aggregate_daily(
        self,
        entries: List['UsageEntry'],
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None
    ) -> List[Dict[str, Any]]:
        '''Aggregate usage data by day.'''
        def day_key(ts: datetime) -> str:
            return ts.strftime('%Y-%m-%d')
        return self._aggregate_by_period(entries, day_key, 'date', start_date, end_date)

    def aggregate_monthly(
        self,
        entries: List['UsageEntry'],
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None
    ) -> List[Dict[str, Any]]:
        '''Aggregate usage data by month.'''
        def month_key(ts: datetime) -> str:
            return ts.strftime('%Y-%m')
        return self._aggregate_by_period(entries, month_key, 'month', start_date, end_date)

    def aggregate_from_blocks(
        self,
        blocks: List['SessionBlock'],
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
        total_usage = sum(item.get('total_usage', 0)
                          for item in aggregated_data)
        total_entries = sum(item.get('entry_count', 0)
                            for item in aggregated_data)
        all_users = set()
        for item in aggregated_data:
            # If you want unique users across all periods, you need to collect user_ids
            # But since only unique_users count is available, we can't get the actual user_ids
            # So we sum unique_users as an approximation (may overcount)
            pass
        # For unique users, we can't get the actual set unless we keep user_ids per period
        # So we just sum unique_users as a rough metric
        total_unique_users = sum(item.get('unique_users', 0)
                                 for item in aggregated_data)
        return {
            'total_usage': total_usage,
            'total_entries': total_entries,
            'total_unique_users': total_unique_users
        }

    def aggregate(self, entries: List['UsageEntry'], start_date: Optional[datetime] = None, end_date: Optional[datetime] = None) -> List[Dict[str, Any]]:
        '''Main aggregation method that reads data and returns aggregated results.'''
        if self.aggregation_mode == 'daily':
            return self.aggregate_daily(entries, start_date, end_date)
        elif self.aggregation_mode == 'monthly':
            return self.aggregate_monthly(entries, start_date, end_date)
        else:
            raise ValueError(
                f"Unknown aggregation_mode: {self.aggregation_mode}")
