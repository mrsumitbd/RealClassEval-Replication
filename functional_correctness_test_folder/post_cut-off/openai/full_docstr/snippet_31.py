
import os
import json
from datetime import datetime, timezone, timedelta
from typing import List, Dict, Any, Callable, Optional
from zoneinfo import ZoneInfo


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
        if aggregation_mode not in ('daily', 'monthly'):
            raise ValueError("aggregation_mode must be 'daily' or 'monthly'")
        self.aggregation_mode = aggregation_mode
        try:
            self.tz = ZoneInfo(timezone)
        except Exception:
            self.tz = timezone.utc

    def _parse_timestamp(self, ts: str) -> datetime:
        dt = datetime.fromisoformat(ts)
        if dt.tzinfo is None:
            dt = dt.replace(tzinfo=timezone.utc)
        return dt.astimezone(self.tz)

    def _aggregate_by_period(
        self,
        entries: List[Dict[str, Any]],
        period_key_func: Callable[[datetime], str],
        period_type: str,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None
    ) -> List[Dict[str, Any]]:
        '''Generic aggregation by time period.'''
        # Filter entries by date range
        filtered = []
        for e in entries:
            ts = self._parse_timestamp(e['timestamp'])
            if start_date and ts < start_date:
                continue
            if end_date and ts > end_date:
                continue
            filtered.append((ts, e))

        # Group by period key
        agg: Dict[str, Dict[str, Any]] = {}
        for ts, e in filtered:
            key = period_key_func(ts)
            if key not in agg:
                agg[key] = {'period': key, 'total_usage': 0.0, 'count': 0}
            usage = float(e.get('usage', 0))
            agg[key]['total_usage'] += usage
            agg[key]['count'] += 1

        # Convert to list sorted by period
        result = list(agg.values())
        result.sort(key=lambda x: x['period'])
        return result

    def aggregate_daily(
        self,
        entries: List[Dict[str, Any]],
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None
    ) -> List[Dict[str, Any]]:
        '''Aggregate usage data by day.'''
        return self._aggregate_by_period(
            entries,
            period_key_func=lambda dt: dt.strftime('%Y-%m-%d'),
            period_type='date',
            start_date=start_date,
            end_date=end_date
        )

    def aggregate_monthly(
        self,
        entries: List[Dict[str, Any]],
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None
    ) -> List[Dict[str, Any]]:
        '''Aggregate usage data by month.'''
        return self._aggregate_by_period(
            entries,
            period_key_func=lambda dt: dt.strftime('%Y-%m'),
            period_type='month',
            start_date=start_date,
            end_date=end_date
        )

    def aggregate_from_blocks(
        self,
        blocks: List[Dict[str, Any]],
        view_type: str = 'daily'
    ) -> List[Dict[str, Any]]:
        '''Aggregate data from session blocks.'''
        # Convert blocks to entries
        entries = []
        for b in blocks:
            start_ts = b.get('start_time')
            if not start_ts:
                continue
            entries.append({
                'timestamp': start_ts,
                'usage': b.get('usage', 0)
            })
        if view_type == 'daily':
            return self.aggregate_daily(entries)
        elif view_type == 'monthly':
            return self.aggregate_monthly(entries)
        else:
            raise ValueError("view_type must be 'daily' or 'monthly'")

    def calculate_totals(self, aggregated_data: List[Dict[str, Any]]) -> Dict[str, Any]:
        '''Calculate totals from aggregated data.'''
        total_usage = sum(d.get('total_usage', 0) for d in aggregated_data)
        total_count = sum(d.get('count', 0) for d in aggregated_data)
        avg_usage = total_usage / total_count if total_count else 0
        return {
            'total_usage': total_usage,
            'total_count': total_count,
            'average_usage': avg_usage
        }

    def _load_entries(self) -> List[Dict[str, Any]]:
        '''Load usage entries from JSON files in data_path.'''
        entries: List[Dict[str, Any]] = []
        for root, _, files in os.walk(self.data_path):
            for f in files:
                if f.lower().endswith('.json'):
                    path = os.path.join(root, f)
                    try:
                        with open(path, 'r', encoding='utf-8') as fh:
                            data = json.load(fh)
                            if isinstance(data, list):
                                entries.extend(data)
                            elif isinstance(data, dict):
                                entries.append(data)
                    except Exception:
                        continue
        return entries

    def aggregate(self, start_date: Optional[datetime] = None, end_date: Optional[datetime] = None) -> List[Dict[str, Any]]:
        '''Main aggregation method that reads data and returns aggregated results.'''
        entries = self._load_entries()
        if self.aggregation_mode == 'daily':
            return self.aggregate_daily(entries, start_date, end_date)
        else:
            return self.aggregate_monthly(entries, start_date, end_date)
