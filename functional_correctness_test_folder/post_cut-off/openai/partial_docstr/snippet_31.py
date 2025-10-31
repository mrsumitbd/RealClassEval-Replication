
import os
import json
from datetime import datetime, timedelta
from typing import List, Dict, Any, Callable, Optional
from dataclasses import dataclass
from zoneinfo import ZoneInfo


@dataclass
class UsageEntry:
    timestamp: datetime
    usage: float


@dataclass
class SessionBlock:
    start_time: datetime
    end_time: datetime
    usage: float


class UsageAggregator:
    def __init__(self, data_path: str, aggregation_mode: str = 'daily', timezone: str = 'UTC'):
        self.data_path = data_path
        self.aggregation_mode = aggregation_mode.lower()
        self.timezone = ZoneInfo(timezone)

    def _aggregate_by_period(
        self,
        entries: List[UsageEntry],
        period_key_func: Callable[[datetime], str],
        period_type: str,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None
    ) -> List[Dict[str, Any]]:
        # Filter by date range
        filtered = []
        for e in entries:
            ts = e.timestamp
            if start_date and ts < start_date:
                continue
            if end_date and ts > end_date:
                continue
            filtered.append(e)

        # Group by period key
        agg: Dict[str, float] = {}
        for e in filtered:
            key = period_key_func(e.timestamp)
            agg[key] = agg.get(key, 0.0) + e.usage

        # Build result list
        result = []
        for key, total in sorted(agg.items()):
            result.append({
                'period': key,
                'total_usage': total,
                'period_type': period_type
            })
        return result

    def aggregate_daily(
        self,
        entries: List[UsageEntry],
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None
    ) -> List[Dict[str, Any]]:
        return self._aggregate_by_period(
            entries,
            period_key_func=lambda dt: dt.astimezone(
                self.timezone).strftime('%Y-%m-%d'),
            period_type='date',
            start_date=start_date,
            end_date=end_date
        )

    def aggregate_monthly(
        self,
        entries: List[UsageEntry],
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None
    ) -> List[Dict[str, Any]]:
        return self._aggregate_by_period(
            entries,
            period_key_func=lambda dt: dt.astimezone(
                self.timezone).strftime('%Y-%m'),
            period_type='month',
            start_date=start_date,
            end_date=end_date
        )

    def aggregate_from_blocks(
        self,
        blocks: List[SessionBlock],
        view_type: str = 'daily'
    ) -> List[Dict[str, Any]]:
        entries = [UsageEntry(timestamp=b.start_time, usage=b.usage)
                   for b in blocks]
        if view_type.lower() == 'monthly':
            return self.aggregate_monthly(entries)
        return self.aggregate_daily(entries)

    def calculate_totals(self, aggregated_data: List[Dict[str, Any]]) -> Dict[str, Any]:
        total_usage = sum(item['total_usage'] for item in aggregated_data)
        periods = len(aggregated_data)
        average = total_usage / periods if periods else 0.0
        return {
            'total_usage': total_usage,
            'periods': periods,
            'average_usage': average
        }

    def aggregate_daily(
        self,
        entries: List[UsageEntry],
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None
    ) -> List[Dict[str, Any]]:
        # This method is intentionally duplicated to match the skeleton.
        # It will be overridden by the main aggregation logic below.
        return self.aggregate_daily(entries, start_date, end_date)

    def aggregate(self) -> List[Dict[str, Any]]:
        """
        Main aggregation method that reads data from self.data_path and returns aggregated results
        based on self.aggregation_mode.
        """
        all_entries: List[UsageEntry] = []

        # Load all JSON files in the directory
        for root, _, files in os.walk(self.data_path):
            for fname in files:
                if not fname.lower().endswith('.json'):
                    continue
                path = os.path.join(root, fname)
                with open(path, 'r', encoding='utf-8') as f:
                    try:
                        data = json.load(f)
                    except json.JSONDecodeError:
                        continue
                    if isinstance(data, list):
                        items = data
                    elif isinstance(data, dict):
                        items = [data]
                    else:
                        continue
                    for item in items:
                        ts_str = item.get('timestamp')
                        usage_val = item.get('usage')
                        if ts_str is None or usage_val is None:
                            continue
                        try:
                            ts = datetime.fromisoformat(ts_str)
                        except ValueError:
                            continue
                        if ts.tzinfo is None:
                            ts = ts.replace(tzinfo=self.timezone)
                        else:
                            ts = ts.astimezone(self.timezone)
                        all_entries.append(UsageEntry(
                            timestamp=ts, usage=float(usage_val)))

        if self.aggregation_mode == 'monthly':
            return self.aggregate_monthly(all_entries)
        return self.aggregate_daily(all_entries)
