
import os
from typing import List, Dict, Any, Callable, Optional
from datetime import datetime
import pytz
from collections import defaultdict

# Dummy classes for type hints (remove if you have real ones)


class UsageEntry:
    def __init__(self, timestamp: datetime, usage: float):
        self.timestamp = timestamp
        self.usage = usage


class SessionBlock:
    def __init__(self, entries: List[UsageEntry]):
        self.entries = entries


class UsageAggregator:

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
        entries: List[UsageEntry],
        period_key_func: Callable[[datetime], str],
        period_type: str,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None
    ) -> List[Dict[str, Any]]:
        '''Generic aggregation by time period.'''
        period_data = defaultdict(list)
        for entry in entries:
            ts = entry.timestamp
            if ts.tzinfo is None:
                ts = pytz.UTC.localize(ts)
            ts = ts.astimezone(self.timezone)
            if start_date:
                if start_date.tzinfo is None:
                    start_date = pytz.UTC.localize(start_date)
                if ts < start_date.astimezone(self.timezone):
                    continue
            if end_date:
                if end_date.tzinfo is None:
                    end_date = pytz.UTC.localize(end_date)
                if ts > end_date.astimezone(self.timezone):
                    continue
            key = period_key_func(ts)
            period_data[key].append(entry.usage)
        result = []
        for key in sorted(period_data.keys()):
            usages = period_data[key]
            result.append({
                period_type: key,
                'total_usage': sum(usages),
                'count': len(usages),
                'average_usage': sum(usages)/len(usages) if usages else 0.0
            })
        return result

    def aggregate_daily(
        self,
        entries: List[UsageEntry],
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None
    ) -> List[Dict[str, Any]]:
        '''Aggregate usage data by day.'''
        def day_key(ts: datetime) -> str:
            return ts.strftime('%Y-%m-%d')
        return self._aggregate_by_period(
            entries, day_key, 'date', start_date, end_date
        )

    def aggregate_monthly(
        self,
        entries: List[UsageEntry],
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None
    ) -> List[Dict[str, Any]]:
        '''Aggregate usage data by month.'''
        def month_key(ts: datetime) -> str:
            return ts.strftime('%Y-%m')
        return self._aggregate_by_period(
            entries, month_key, 'month', start_date, end_date
        )

    def aggregate_from_blocks(
        self,
        blocks: List[SessionBlock],
        view_type: str = 'daily'
    ) -> List[Dict[str, Any]]:
        '''Aggregate data from session blocks.'''
        all_entries = []
        for block in blocks:
            all_entries.extend(block.entries)
        if view_type == 'daily':
            return self.aggregate_daily(all_entries)
        elif view_type == 'monthly':
            return self.aggregate_monthly(all_entries)
        else:
            raise ValueError("view_type must be 'daily' or 'monthly'")

    def calculate_totals(
        self,
        aggregated_data: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        '''Calculate totals from aggregated data.'''
        total_usage = sum(item['total_usage'] for item in aggregated_data)
        total_count = sum(item['count'] for item in aggregated_data)
        average_usage = total_usage / total_count if total_count else 0.0
        return {
            'total_usage': total_usage,
            'total_count': total_count,
            'average_usage': average_usage
        }

    def aggregate(self,
                  entries: List[UsageEntry],
                  start_date: Optional[datetime] = None,
                  end_date: Optional[datetime] = None
                  ) -> List[Dict[str, Any]]:
        '''Main aggregation method that reads data and returns aggregated results.'''
        if self.aggregation_mode == 'daily':
            return self.aggregate_daily(entries, start_date, end_date)
        elif self.aggregation_mode == 'monthly':
            return self.aggregate_monthly(entries, start_date, end_date)
        else:
            raise ValueError("aggregation_mode must be 'daily' or 'monthly'")
