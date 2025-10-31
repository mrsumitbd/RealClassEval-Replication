from __future__ import annotations

from typing import Any, Callable, Dict, List, Optional
from datetime import datetime
from collections import defaultdict

try:
    from zoneinfo import ZoneInfo
except Exception:  # pragma: no cover
    ZoneInfo = None  # type: ignore[attr-defined]


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
        if aggregation_mode not in {'daily', 'monthly'}:
            raise ValueError("aggregation_mode must be 'daily' or 'monthly'")
        self.aggregation_mode = aggregation_mode
        if ZoneInfo is None:
            self.tz = None
        else:
            try:
                self.tz = ZoneInfo(timezone)
            except Exception as e:  # pragma: no cover
                raise ValueError(f"Invalid timezone: {timezone}") from e

    def _to_tz(self, ts: datetime) -> datetime:
        if self.tz is None:
            return ts
        if ts.tzinfo is None:
            # assume UTC naive
            return ts.replace(tzinfo=ZoneInfo('UTC')).astimezone(self.tz)
        return ts.astimezone(self.tz)

    def _extract_timestamp(self, obj: Any) -> Optional[datetime]:
        # Common keys/attrs that might contain timestamps
        candidates = ['timestamp', 'time', 'ts',
                      'created_at', 'start', 'start_time', 'datetime']
        val = None
        if isinstance(obj, dict):
            for k in candidates:
                if k in obj:
                    val = obj[k]
                    break
        else:
            for k in candidates:
                if hasattr(obj, k):
                    val = getattr(obj, k)
                    break
        if val is None:
            return None
        if isinstance(val, datetime):
            return val
        if isinstance(val, (int, float)):
            try:
                return datetime.fromtimestamp(float(val))
            except Exception:
                return None
        if isinstance(val, str):
            try:
                # Prefer fromisoformat; for strings with Z, replace Z
                s = val.strip()
                if s.endswith('Z'):
                    s = s[:-1] + '+00:00'
                return datetime.fromisoformat(s)
            except Exception:
                return None
        return None

    def _entry_to_numeric_fields(self, entry: Any) -> Dict[str, float]:
        # Returns numeric fields to aggregate from an entry (excluding time-like keys)
        skip_keys = {'timestamp', 'time', 'ts',
                     'created_at', 'start', 'start_time', 'datetime'}
        out: Dict[str, float] = {}
        if isinstance(entry, dict):
            items = entry.items()
        else:
            # Collect public attributes (exclude callables/private)
            items = ((k, getattr(entry, k)) for k in dir(entry)
                     if not k.startswith('_') and hasattr(entry, k))
        for k, v in items:
            if k in skip_keys:
                continue
            if isinstance(v, (int, float)) and not isinstance(v, bool):
                out[k] = float(v)
        return out

    def _aggregate_by_period(
        self,
        entries: List["UsageEntry"],
        period_key_func: Callable[[datetime], str],
        period_type: str,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None
    ) -> List[Dict[str, Any]]:
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
        # Normalize date filters into timezone
        if start_date is not None:
            start_in_tz = self._to_tz(start_date)
        else:
            start_in_tz = None
        if end_date is not None:
            end_in_tz = self._to_tz(end_date)
        else:
            end_in_tz = None

        groups: Dict[str, Dict[str, float]] = defaultdict(
            lambda: defaultdict(float))
        counts: Dict[str, int] = defaultdict(int)
        all_numeric_keys: set[str] = set()

        for e in entries or []:
            ts = self._extract_timestamp(e)
            if ts is None:
                continue
            ts_tz = self._to_tz(ts)
            if start_in_tz is not None and ts_tz < start_in_tz:
                continue
            if end_in_tz is not None and ts_tz > end_in_tz:
                continue
            period_key = period_key_func(ts_tz)
            counts[period_key] += 1
            nums = self._entry_to_numeric_fields(e)
            for k, v in nums.items():
                groups[period_key][k] += v
                all_numeric_keys.add(k)

        # Build results sorted by period key
        results: List[Dict[str, Any]] = []
        for key in sorted(groups.keys()):
            row: Dict[str, Any] = {period_type: key, 'count': counts[key]}
            # ensure stable order, iterate sorted numeric keys
            for metric in sorted(all_numeric_keys):
                row[metric] = groups[key].get(metric, 0.0)
            results.append(row)
        # Include periods with counts but no numeric metrics
        orphan_periods = sorted(set(counts.keys()) - set(groups.keys()))
        for key in orphan_periods:
            results.append({period_type: key, 'count': counts[key]})
        # Re-sort to maintain chronological order
        results.sort(key=lambda d: d[period_type])
        return results

    def aggregate_daily(
        self,
        entries: List["UsageEntry"],
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None
    ) -> List[Dict[str, Any]]:
        """Aggregate usage data by day.
        Args:
            entries: List of usage entries
            start_date: Optional start date filter
            end_date: Optional end date filter
        Returns:
            List of daily aggregated data
        """
        def day_key(ts: datetime) -> str:
            return self._to_tz(ts).strftime('%Y-%m-%d')

        return self._aggregate_by_period(entries, day_key, 'date', start_date, end_date)

    def aggregate_monthly(
        self,
        entries: List["UsageEntry"],
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None
    ) -> List[Dict[str, Any]]:
        """Aggregate usage data by month.
        Args:
            entries: List of usage entries
            start_date: Optional start date filter
            end_date: Optional end date filter
        Returns:
            List of monthly aggregated data
        """
        def month_key(ts: datetime) -> str:
            return self._to_tz(ts).strftime('%Y-%m')

        return self._aggregate_by_period(entries, month_key, 'month', start_date, end_date)

    def aggregate_from_blocks(self, blocks: List["SessionBlock"], view_type: str = 'daily') -> List[Dict[str, Any]]:
        """Aggregate data from session blocks.
        Args:
            blocks: List of session blocks
            view_type: Type of aggregation ('daily' or 'monthly')
        Returns:
            List of aggregated data
        """
        entries: List[Any] = []

        for b in blocks or []:
            # Try common containers: dict or object
            container = None
            if isinstance(b, dict):
                for key in ('entries', 'usages', 'usage', 'events', 'records'):
                    if key in b and isinstance(b[key], list):
                        container = b[key]
                        break
            else:
                for key in ('entries', 'usages', 'usage', 'events', 'records'):
                    if hasattr(b, key) and isinstance(getattr(b, key), list):
                        container = getattr(b, key)
                        break
            if container is not None:
                entries.extend(container)
                continue

            # Fallback: treat the block itself as a single entry if it has a timestamp
            if self._extract_timestamp(b) is not None:
                entries.append(b)

        if view_type not in {'daily', 'monthly'}:
            raise ValueError("view_type must be 'daily' or 'monthly'")

        if view_type == 'daily':
            return self.aggregate_daily(entries)
        return self.aggregate_monthly(entries)

    def calculate_totals(self, aggregated_data: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Calculate totals from aggregated data.
        Args:
            aggregated_data: List of aggregated daily or monthly data
        Returns:
            Dictionary with total statistics
        """
        if not aggregated_data:
            return {'periods': 0, 'count': 0}

        totals: Dict[str, Any] = {}
        totals['periods'] = len(aggregated_data)

        # Determine period key name
        period_key = 'date' if 'date' in aggregated_data[
            0] else 'month' if 'month' in aggregated_data[0] else None
        if period_key:
            periods_sorted = sorted(
                aggregated_data, key=lambda d: d[period_key])
            totals['start'] = periods_sorted[0][period_key]
            totals['end'] = periods_sorted[-1][period_key]

        # Sum numeric fields across rows
        numeric_keys: set[str] = set()
        for row in aggregated_data:
            for k, v in row.items():
                if k == period_key:
                    continue
                if isinstance(v, (int, float)) and not isinstance(v, bool):
                    numeric_keys.add(k)
        for k in numeric_keys:
            totals[k] = sum(float(row.get(k, 0.0)) for row in aggregated_data)

        # Backward-compatible alias
        if 'count' in totals:
            totals['total_count'] = totals['count']

        return totals

    def aggregate_daily(  # type: ignore[no-redef]
        self,
        entries: List["UsageEntry"],
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None
    ) -> List[Dict[str, Any]]:
        """Main aggregation method that reads data and returns aggregated results.
        Returns:
            List of aggregated data based on aggregation_mode
        """
        if self.aggregation_mode == 'daily':
            return self._aggregate_by_period(
                entries,
                lambda ts: self._to_tz(ts).strftime('%Y-%m-%d'),
                'date',
                start_date,
                end_date,
            )
        elif self.aggregation_mode == 'monthly':
            return self._aggregate_by_period(
                entries,
                lambda ts: self._to_tz(ts).strftime('%Y-%m'),
                'month',
                start_date,
                end_date,
            )
        else:  # pragma: no cover
            raise ValueError(
                f"Unsupported aggregation_mode: {self.aggregation_mode}")
