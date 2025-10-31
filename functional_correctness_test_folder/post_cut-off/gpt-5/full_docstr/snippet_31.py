from __future__ import annotations

from typing import Any, Callable, Dict, List, Optional, Iterable, Tuple
from datetime import datetime, timezone as dt_timezone
import math

try:
    from zoneinfo import ZoneInfo
except Exception:  # pragma: no cover
    ZoneInfo = None  # type: ignore


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
        self.aggregation_mode = aggregation_mode if aggregation_mode in (
            'daily', 'monthly') else 'daily'
        self.timezone_name = timezone or 'UTC'
        self.tzinfo = self._resolve_tz(self.timezone_name)

    # --------- Helpers ---------

    @staticmethod
    def _resolve_tz(tzname: str):
        if ZoneInfo is not None:
            try:
                return ZoneInfo(tzname)
            except Exception:
                return ZoneInfo('UTC')
        # Fallback to naive UTC if zoneinfo not available
        return dt_timezone.utc

    def _ensure_aware(self, dt: datetime) -> datetime:
        if dt is None:
            return None  # type: ignore
        if dt.tzinfo is None:
            # Assume provided timestamp is UTC if naive
            dt = dt.replace(tzinfo=dt_timezone.utc)
        return dt.astimezone(self.tzinfo)

    @staticmethod
    def _is_number(v: Any) -> bool:
        return isinstance(v, (int, float)) and not isinstance(v, bool) and not (isinstance(v, float) and (math.isnan(v) or math.isinf(v)))

    @staticmethod
    def _as_mapping(obj: Any) -> Dict[str, Any]:
        if obj is None:
            return {}
        if isinstance(obj, dict):
            return obj
        # Try dataclass-like / object attributes
        try:
            return {k: getattr(obj, k) for k in dir(obj) if not k.startswith('_') and not callable(getattr(obj, k))}
        except Exception:
            try:
                return vars(obj)
            except Exception:
                return {}

    @staticmethod
    def _find_timestamp(mapping: Dict[str, Any]) -> Optional[datetime]:
        candidate_keys = ('timestamp', 'time', 'datetime',
                          'created_at', 'created', 'ts', 'start', 'started_at')
        for key in candidate_keys:
            if key in mapping:
                val = mapping[key]
                if isinstance(val, datetime):
                    return val
        # Sometimes nested under 'meta' etc.
        for key in ('meta', 'info'):
            sub = mapping.get(key)
            if isinstance(sub, dict):
                for k2 in ('timestamp', 'time', 'datetime'):
                    val = sub.get(k2)
                    if isinstance(val, datetime):
                        return val
        return None

    @staticmethod
    def _numeric_fields(mapping: Dict[str, Any], exclude: Iterable[str]) -> Dict[str, float]:
        out: Dict[str, float] = {}
        for k, v in mapping.items():
            if k in exclude:
                continue
            if UsageAggregator._is_number(v):
                out[k] = float(v)
        return out

    def _period_key_funcs(self) -> Tuple[Callable[[datetime], str], Callable[[datetime], str]]:
        def key_date(dt: datetime) -> str:
            return dt.astimezone(self.tzinfo).strftime('%Y-%m-%d')

        def key_month(dt: datetime) -> str:
            return dt.astimezone(self.tzinfo).strftime('%Y-%m')

        return key_date, key_month

    def _date_in_range(self, ts: datetime, start_date: Optional[datetime], end_date: Optional[datetime]) -> bool:
        if start_date is not None and ts < start_date:
            return False
        if end_date is not None and ts > end_date:
            return False
        return True

    # --------- Core aggregation ---------

    def _aggregate_by_period(
        self,
        entries: List[Any],
        period_key_func: Callable[[datetime], str],
        period_type: str,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None
    ) -> List[Dict[str, Any]]:
        '''Generic aggregation by time period.
        Args:
            entries: List of usage entries
            period_key_func: Function to extract period key from timestamp
            period_type: Type of period ('date' or 'month')
            start_date: Optional start date filter
            end_date: Optional end date filter
        Returns:
            List of aggregated data dictionaries
        '''
        start_date = self._ensure_aware(start_date) if start_date else None
        end_date = self._ensure_aware(end_date) if end_date else None

        groups: Dict[str, Dict[str, Any]] = {}

        for entry in entries or []:
            mapping = self._as_mapping(entry)
            ts = self._find_timestamp(mapping)
            if ts is None:
                # Skip entries without timestamp
                continue
            ts = self._ensure_aware(ts)
            if not self._date_in_range(ts, start_date, end_date):
                continue

            key = period_key_func(ts)
            bucket = groups.get(key)
            if bucket is None:
                bucket = {'period': key,
                          'period_type': period_type, 'count': 0}
                groups[key] = bucket

            bucket['count'] += 1

            # Sum numeric fields (top-level only)
            numeric = self._numeric_fields(mapping, exclude={'timestamp', 'time', 'datetime', 'created_at',
                                           'created', 'ts', 'start', 'started_at', 'end', 'ended_at', 'period', 'period_type', 'count'})
            for k, v in numeric.items():
                bucket[k] = bucket.get(k, 0.0) + v

        # Sort by period key ascending
        result = [groups[k] for k in sorted(groups.keys())]
        return result

    def _aggregate_daily_entries(self, entries: List[Any], start_date: Optional[datetime] = None, end_date: Optional[datetime] = None) -> List[Dict[str, Any]]:
        key_date, _ = self._period_key_funcs()
        return self._aggregate_by_period(entries, key_date, 'date', start_date=start_date, end_date=end_date)

    def _aggregate_monthly_entries(self, entries: List[Any], start_date: Optional[datetime] = None, end_date: Optional[datetime] = None) -> List[Dict[str, Any]]:
        _, key_month = self._period_key_funcs()
        return self._aggregate_by_period(entries, key_month, 'month', start_date=start_date, end_date=end_date)

    def aggregate_monthly(self, entries: List[Any], start_date: Optional[datetime] = None, end_date: Optional[datetime] = None) -> List[Dict[str, Any]]:
        '''Aggregate usage data by month.
        Args:
            entries: List of usage entries
            start_date: Optional start date filter
            end_date: Optional end date filter
        Returns:
            List of monthly aggregated data
        '''
        return self._aggregate_monthly_entries(entries, start_date=start_date, end_date=end_date)

    def aggregate_from_blocks(self, blocks: List[Any], view_type: str = 'daily') -> List[Dict[str, Any]]:
        '''Aggregate data from session blocks.
        Args:
            blocks: List of session blocks
            view_type: Type of aggregation ('daily' or 'monthly')
        Returns:
            List of aggregated data
        '''
        if not blocks:
            return []

        synthesized_entries: List[Dict[str, Any]] = []

        for block in blocks:
            bmap = self._as_mapping(block)

            # If block has entries, extend directly
            entries_attr = bmap.get('entries') or bmap.get(
                'usage') or bmap.get('events')
            if isinstance(entries_attr, list) and entries_attr:
                for e in entries_attr:
                    em = self._as_mapping(e)
                    # Ensure there is a timestamp present; try to infer from block if missing
                    if self._find_timestamp(em) is None:
                        ts = self._find_timestamp(bmap)
                        if ts is not None:
                            em = dict(em)
                            em['timestamp'] = ts
                    synthesized_entries.append(em)
                continue

            # Otherwise synthesize a single entry from the block
            ts = self._find_timestamp(bmap)
            if ts is None:
                # If still missing, skip this block
                continue

            numeric = self._numeric_fields(bmap, exclude={'timestamp', 'time', 'datetime', 'created_at', 'created', 'ts', 'start',
                                           'started_at', 'end', 'ended_at', 'period', 'period_type', 'count', 'entries', 'usage', 'events', 'stats', 'metrics'})
            # If block carries a 'stats' or 'metrics' dict, include their numeric fields too
            for subkey in ('stats', 'metrics', 'totals'):
                sub = bmap.get(subkey)
                if isinstance(sub, dict):
                    for k, v in self._numeric_fields(sub, exclude=()).items():
                        numeric[k] = numeric.get(k, 0.0) + v

            synthesized_entries.append({'timestamp': ts, **numeric})

        if view_type == 'monthly':
            return self._aggregate_monthly_entries(synthesized_entries)
        # default daily
        return self._aggregate_daily_entries(synthesized_entries)

    def calculate_totals(self, aggregated_data: List[Dict[str, Any]]) -> Dict[str, Any]:
        '''Calculate totals from aggregated data.
        Args:
            aggregated_data: List of aggregated daily or monthly data
        Returns:
            Dictionary with total statistics
        '''
        totals: Dict[str, Any] = {'periods': len(aggregated_data or [])}
        if not aggregated_data:
            totals['count'] = 0
            return totals

        keys_to_sum: List[str] = []
        # Determine numeric keys across data
        for row in aggregated_data:
            for k, v in row.items():
                if k in ('period', 'period_type'):
                    continue
                if self._is_number(v):
                    if k not in keys_to_sum:
                        keys_to_sum.append(k)

        for k in keys_to_sum:
            totals[k] = 0.0

        for row in aggregated_data:
            for k in keys_to_sum:
                v = row.get(k)
                if self._is_number(v):
                    totals[k] += float(v)

        # Normalize 'count' as int if present
        if 'count' in totals:
            try:
                totals['count'] = int(totals['count'])
            except Exception:
                pass

        return totals

    def aggregate_daily(self, entries: List[Any], start_date: Optional[datetime] = None, end_date: Optional[datetime] = None) -> List[Dict[str, Any]]:
        '''Main aggregation method that reads data and returns aggregated results.
        Returns:
            List of aggregated data based on aggregation_mode
        '''
        if self.aggregation_mode == 'monthly':
            return self._aggregate_monthly_entries(entries, start_date=start_date, end_date=end_date)
        return self._aggregate_daily_entries(entries, start_date=start_date, end_date=end_date)
