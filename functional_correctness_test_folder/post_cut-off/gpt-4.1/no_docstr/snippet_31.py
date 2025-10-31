
from typing import List, Dict, Any, Callable, Optional
from datetime import datetime, timedelta
import pytz
from collections import defaultdict

# Dummy classes for type hints (replace with actual implementations)


class UsageEntry:
    def __init__(self, timestamp: datetime, usage: float):
        self.timestamp = timestamp
        self.usage = usage


class SessionBlock:
    def __init__(self, start: datetime, end: datetime, usage: float):
        self.start = start
        self.end = end
        self.usage = usage


class UsageAggregator:

    def __init__(self, data_path: str, aggregation_mode: str = 'daily', timezone: str = 'UTC'):
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
        period_data = defaultdict(float)
        for entry in entries:
            ts = entry.timestamp.astimezone(self.timezone)
            if start_date and ts < start_date:
                continue
            if end_date and ts > end_date:
                continue
            key = period_key_func(ts)
            period_data[key] += entry.usage
        result = []
        for key in sorted(period_data.keys()):
            result.append({
                period_type: key,
                'usage': period_data[key]
            })
        return result

    def aggregate_daily(
        self,
        entries: List[UsageEntry],
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None
    ) -> List[Dict[str, Any]]:
        def day_key(dt: datetime) -> str:
            return dt.strftime('%Y-%m-%d')
        return self._aggregate_by_period(
            entries, day_key, 'date', start_date, end_date
        )

    def aggregate_monthly(
        self,
        entries: List[UsageEntry],
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None
    ) -> List[Dict[str, Any]]:
        def month_key(dt: datetime) -> str:
            return dt.strftime('%Y-%m')
        return self._aggregate_by_period(
            entries, month_key, 'month', start_date, end_date
        )

    def aggregate_from_blocks(
        self,
        blocks: List[SessionBlock],
        view_type: str = 'daily'
    ) -> List[Dict[str, Any]]:
        entries = []
        for block in blocks:
            # For simplicity, assign usage to the start time of the block
            entries.append(UsageEntry(block.start, block.usage))
        if view_type == 'daily':
            return self.aggregate_daily(entries)
        elif view_type == 'monthly':
            return self.aggregate_monthly(entries)
        else:
            raise ValueError(f"Unknown view_type: {view_type}")

    def calculate_totals(
        self,
        aggregated_data: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        total_usage = sum(item['usage'] for item in aggregated_data)
        return {'total_usage': total_usage}

    def aggregate_daily(
        self,
        entries: List[UsageEntry],
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None
    ) -> List[Dict[str, Any]]:
        def day_key(dt: datetime) -> str:
            return dt.strftime('%Y-%m-%d')
        return self._aggregate_by_period(
            entries, day_key, 'date', start_date, end_date
        )
