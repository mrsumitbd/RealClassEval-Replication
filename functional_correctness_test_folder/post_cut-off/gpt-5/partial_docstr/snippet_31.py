from __future__ import annotations

from datetime import datetime
from typing import Any, Callable, Dict, List, Optional
from numbers import Number

try:
    from zoneinfo import ZoneInfo
except Exception:
    ZoneInfo = None  # type: ignore


class UsageAggregator:
    def __init__(self, data_path: str, aggregation_mode: str = 'daily', timezone: str = 'UTC'):
        self.data_path = data_path
        if aggregation_mode not in ('daily', 'monthly'):
            raise ValueError("aggregation_mode must be 'daily' or 'monthly'")
        self.aggregation_mode = aggregation_mode
        self.timezone = timezone
        if ZoneInfo is None:
            self._tzinfo = None
        else:
            try:
                self._tzinfo = ZoneInfo(timezone)
            except Exception:
                self._tzinfo = ZoneInfo("UTC")

    def _to_local(self, dt: datetime) -> datetime:
        if self._tzinfo is None:
            return dt
        if dt.tzinfo is None:
            dt = dt.replace(tzinfo=ZoneInfo("UTC"))
        return dt.astimezone(self._tzinfo)

    def _extract_timestamp(self, obj: Any) -> Optional[datetime]:
        # Try attribute access first
        ts = getattr(obj, 'timestamp', None)
        if isinstance(ts, datetime):
            return ts
        # Try mapping-style access
        if isinstance(obj, dict):
            ts = obj.get('timestamp')
            if isinstance(ts, datetime):
                return ts
        return None

    def _to_mapping(self, obj: Any) -> Dict[str, Any]:
        if isinstance(obj, dict):
            return obj
        # Dataclass or simple object fallback
        d = {}
        for k in dir(obj):
            if k.startswith('_'):
                continue
            try:
                v = getattr(obj, k)
            except Exception:
                continue
            # Skip callables and descriptors
            if callable(v):
                continue
            d[k] = v
        return d

    def _aggregate_by_period(
        self,
        entries: List[Any],
        period_key_func: Callable[[datetime], str],
        period_type: str,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None
    ) -> List[Dict[str, Any]]:
        if start_date is not None:
            start_local = self._to_local(start_date)
        else:
            start_local = None
        if end_date is not None:
            end_local = self._to_local(end_date)
        else:
            end_local = None

        buckets: Dict[str, Dict[str, Any]] = {}

        for entry in entries:
            ts = self._extract_timestamp(entry)
            if not isinstance(ts, datetime):
                continue
            local_ts = self._to_local(ts)

            if start_local and local_ts < start_local:
                continue
            if end_local and local_ts > end_local:
                continue

            key = period_key_func(local_ts)
            if key not in buckets:
                buckets[key] = {
                    period_type: key,
                    'count': 0,
                }

            # Convert entry to mapping and aggregate numeric fields
            mapping = self._to_mapping(entry)
            for k, v in mapping.items():
                if k in ('timestamp', period_type):
                    continue
                if isinstance(v, Number):
                    buckets[key][k] = buckets[key].get(k, 0) + v
            buckets[key]['count'] += 1

        # Sort by period key in chronological order when possible
        def parse_key(k: str) -> Any:
            fmt = '%Y-%m-%d' if period_type == 'date' else '%Y-%m'
            try:
                return datetime.strptime(k, fmt)
            except Exception:
                return k

        sorted_items = sorted(
            buckets.values(), key=lambda d: parse_key(d[period_type]))
        return sorted_items

    def aggregate_daily(
        self,
        entries: List[Any],
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None
    ) -> List[Dict[str, Any]]:
        # This definition will be overwritten by the later duplicate in the skeleton.
        # Implemented via helper to be callable by the final dispatcher.
        return self._aggregate_daily_entries(entries, start_date, end_date)

    def _aggregate_daily_entries(
        self,
        entries: List[Any],
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None
    ) -> List[Dict[str, Any]]:
        return self._aggregate_by_period(
            entries,
            period_key_func=lambda dt: dt.strftime('%Y-%m-%d'),
            period_type='date',
            start_date=start_date,
            end_date=end_date
        )

    def aggregate_monthly(
        self,
        entries: List[Any],
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None
    ) -> List[Dict[str, Any]]:
        return self._aggregate_by_period(
            entries,
            period_key_func=lambda dt: dt.strftime('%Y-%m'),
            period_type='month',
            start_date=start_date,
            end_date=end_date
        )

    def aggregate_from_blocks(self, blocks: List[Any], view_type: str = 'daily') -> List[Dict[str, Any]]:
        if view_type not in ('daily', 'monthly'):
            raise ValueError("view_type must be 'daily' or 'monthly'")
        if view_type == 'daily':
            return self._aggregate_daily_entries(blocks, None, None)
        return self.aggregate_monthly(blocks, None, None)

    def calculate_totals(self, aggregated_data: List[Dict[str, Any]]) -> Dict[str, Any]:
        totals: Dict[str, Any] = {}
        for item in aggregated_data:
            for k, v in item.items():
                if k in ('date', 'month'):
                    continue
                if isinstance(v, Number):
                    totals[k] = totals.get(k, 0) + v
        return totals

    def aggregate_daily(  # type: ignore[func-returns-value]
        self,
        entries: List[Any],
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None
    ) -> List[Dict[str, Any]]:
        if self.aggregation_mode == 'daily':
            return self._aggregate_daily_entries(entries, start_date, end_date)
        elif self.aggregation_mode == 'monthly':
            return self.aggregate_monthly(entries, start_date, end_date)
        else:
            raise ValueError("Invalid aggregation_mode")
