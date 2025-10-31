from typing import Any, Callable, Dict, Iterable, List, Optional, Union
from datetime import datetime, timezone
import os
import json
import csv

try:
    from zoneinfo import ZoneInfo
except Exception:  # pragma: no cover
    ZoneInfo = None  # type: ignore


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
        self.aggregation_mode = aggregation_mode.lower()
        if self.aggregation_mode not in ('daily', 'monthly'):
            raise ValueError("aggregation_mode must be 'daily' or 'monthly'")

        self.timezone = timezone
        self._tzinfo = self._get_tzinfo(timezone)

    def _get_tzinfo(self, tz: str):
        if ZoneInfo is not None:
            try:
                return ZoneInfo(tz)
            except Exception:
                return ZoneInfo('UTC')
        # Fallback: best-effort UTC if ZoneInfo not available.
        return timezone.utc

    def _ensure_tz(self, dt: datetime) -> datetime:
        if dt.tzinfo is None:
            dt = dt.replace(tzinfo=timezone.utc)
        return dt.astimezone(self._tzinfo)

    def _parse_timestamp(self, entry: Dict[str, Any]) -> datetime:
        # Try common timestamp field names
        candidates = [
            'timestamp', 'ts', 'time', 'created_at', 'createdAt',
            'start_time', 'startTime', 'end_time', 'endTime',
        ]
        for k in candidates:
            if k in entry and entry[k] is not None:
                val = entry[k]
                if isinstance(val, datetime):
                    return self._ensure_tz(val)
                if isinstance(val, (int, float)):
                    # Assume Unix epoch seconds
                    dt = datetime.fromtimestamp(val, tz=timezone.utc)
                    return self._ensure_tz(dt)
                if isinstance(val, str):
                    s = val.strip()
                    # ISO format, allow 'Z'
                    s = s.replace(
                        'Z', '+00:00') if 'Z' in s and '+' not in s else s
                    try:
                        dt = datetime.fromisoformat(s)
                        return self._ensure_tz(dt)
                    except Exception:
                        # Try as int epoch embedded string
                        try:
                            num = float(s)
                            dt = datetime.fromtimestamp(num, tz=timezone.utc)
                            return self._ensure_tz(dt)
                        except Exception:
                            pass
        raise ValueError("Entry missing a recognizable timestamp field")

    def _entry_to_dict(self, e: Any) -> Dict[str, Any]:
        if isinstance(e, dict):
            return dict(e)
        # Try dataclass-like or object with __dict__
        try:
            from dataclasses import asdict, is_dataclass  # type: ignore
            if is_dataclass(e):  # type: ignore
                return asdict(e)  # type: ignore
        except Exception:
            pass
        try:
            return dict(vars(e))
        except Exception:
            pass
        raise TypeError(
            "Unsupported entry type; expected dict-like or object with attributes")

    def _is_numeric(self, v: Any) -> bool:
        # Exclude bool (bool is a subclass of int)
        return (isinstance(v, (int, float)) and not isinstance(v, bool))

    def _in_range(self, dt: datetime, start_date: Optional[datetime], end_date: Optional[datetime]) -> bool:
        if start_date is not None:
            start = self._ensure_tz(start_date)
            if dt < start:
                return False
        if end_date is not None:
            end = self._ensure_tz(end_date)
            if dt > end:
                return False
        return True

    def _aggregate_by_period(
        self,
        entries: List['UsageEntry'],
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
        groups: Dict[str, Dict[str, Any]] = {}

        for raw in entries or []:
            entry = self._entry_to_dict(raw)
            try:
                dt = self._parse_timestamp(entry)
            except Exception:
                # Skip entries we can't parse a timestamp from
                continue
            if not self._in_range(dt, start_date, end_date):
                continue

            key = period_key_func(dt)
            if key not in groups:
                aggr: Dict[str, Any] = {'period': key,
                                        'period_type': period_type, 'count': 0}
                # Convenience alias for consumers that expect 'date' or 'month'
                aggr['date' if period_type == 'date' else 'month'] = key
                groups[key] = aggr

            aggr = groups[key]
            aggr['count'] += 1

            # Sum all numeric fields.
            for k, v in entry.items():
                if k in ('timestamp', 'ts', 'time', 'created_at', 'createdAt', 'start_time', 'startTime', 'end_time', 'endTime'):
                    continue
                if self._is_numeric(v):
                    aggr[k] = aggr.get(k, 0) + float(v)

        # Sort by period key
        result = [groups[k] for k in sorted(groups.keys())]
        return result

    def aggregate_daily(
        self,
        entries: List['UsageEntry'],
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
        # This definition is overridden by the final method below per the provided skeleton.
        # To preserve functionality, the final method will implement both behaviors.
        return self._aggregate_by_period(
            entries,
            lambda d: d.strftime('%Y-%m-%d'),
            'date',
            start_date,
            end_date
        )

    def aggregate_monthly(
        self,
        entries: List['UsageEntry'],
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
        return self._aggregate_by_period(
            entries,
            lambda d: d.strftime('%Y-%m'),
            'month',
            start_date,
            end_date
        )

    def _extract_entries_from_block(self, block: Any) -> List[Dict[str, Any]]:
        # Try common attribute names that may contain entries.
        attr_candidates = ['entries', 'usage',
                           'usage_entries', 'records', 'events', 'data']
        if isinstance(block, dict):
            for k in attr_candidates:
                if k in block and isinstance(block[k], list):
                    return [self._entry_to_dict(e) for e in block[k]]
            # If a block itself resembles an entry
            if any(k in block for k in ('timestamp', 'time', 'ts', 'created_at', 'createdAt', 'start_time', 'startTime')):
                return [self._entry_to_dict(block)]
            return []
        # Object with attributes
        for k in attr_candidates:
            if hasattr(block, k):
                val = getattr(block, k)
                if isinstance(val, list):
                    return [self._entry_to_dict(e) for e in val]
        # If block looks like a single entry
        try:
            d = self._entry_to_dict(block)
            if any(x in d for x in ('timestamp', 'time', 'ts', 'created_at', 'createdAt', 'start_time', 'startTime')):
                return [d]
        except Exception:
            pass
        return []

    def aggregate_from_blocks(self, blocks: List['SessionBlock'], view_type: str = 'daily') -> List[Dict[str, Any]]:
        """Aggregate data from session blocks.
        Args:
            blocks: List of session blocks
            view_type: Type of aggregation ('daily' or 'monthly')
        Returns:
            List of aggregated data
        """
        entries: List[Dict[str, Any]] = []
        for b in blocks or []:
            entries.extend(self._extract_entries_from_block(b))

        mode = (view_type or 'daily').lower()
        if mode == 'monthly':
            return self.aggregate_monthly(entries)
        return self.aggregate_daily(entries)

    def calculate_totals(self, aggregated_data: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Calculate totals from aggregated data.
        Args:
            aggregated_data: List of aggregated daily or monthly data
        Returns:
            Dictionary with total statistics
        """
        totals: Dict[str, Any] = {}
        num_periods = len(aggregated_data or [])
        totals['num_periods'] = num_periods

        # Sum numeric keys across periods (excluding period labels)
        numeric_sums: Dict[str, float] = {}
        for rec in aggregated_data or []:
            for k, v in rec.items():
                if k in ('period', 'period_type', 'date', 'month'):
                    continue
                if isinstance(v, (int, float)) and not isinstance(v, bool):
                    numeric_sums[k] = numeric_sums.get(k, 0.0) + float(v)

        # Copy sums to top-level
        totals.update(numeric_sums)

        # Provide averages per period for numeric fields
        if num_periods > 0:
            averages = {f'avg_{k}_per_period': (
                numeric_sums[k] / num_periods) for k in numeric_sums}
            totals.update(averages)

        return totals

    def _read_entries_from_path(self) -> List[Dict[str, Any]]:
        entries: List[Dict[str, Any]] = []
        if not self.data_path or not os.path.exists(self.data_path):
            return entries

        def read_json_file(fp: str):
            try:
                with open(fp, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                if isinstance(data, list):
                    for e in data:
                        entries.append(self._entry_to_dict(e))
                elif isinstance(data, dict):
                    # If dict contains a list under common keys
                    for k in ('entries', 'usage', 'data', 'records', 'events'):
                        if k in data and isinstance(data[k], list):
                            for e in data[k]:
                                entries.append(self._entry_to_dict(e))
                            break
                    else:
                        entries.append(self._entry_to_dict(data))
            except Exception:
                pass

        def read_jsonl_file(fp: str):
            try:
                with open(fp, 'r', encoding='utf-8') as f:
                    for line in f:
                        s = line.strip()
                        if not s:
                            continue
                        try:
                            e = json.loads(s)
                            entries.append(self._entry_to_dict(e))
                        except Exception:
                            continue
            except Exception:
                pass

        def read_csv_file(fp: str):
            try:
                with open(fp, 'r', encoding='utf-8') as f:
                    reader = csv.DictReader(f)
                    for row in reader:
                        entries.append(dict(row))
            except Exception:
                pass

        if os.path.isdir(self.data_path):
            for root, _, files in os.walk(self.data_path):
                for name in files:
                    fp = os.path.join(root, name)
                    lower = name.lower()
                    if lower.endswith('.jsonl') or lower.endswith('.ndjson'):
                        read_jsonl_file(fp)
                    elif lower.endswith('.json'):
                        read_json_file(fp)
                    elif lower.endswith('.csv'):
                        read_csv_file(fp)
        else:
            fp = self.data_path
            lower = fp.lower()
            if lower.endswith('.jsonl') or lower.endswith('.ndjson'):
                read_jsonl_file(fp)
            elif lower.endswith('.json'):
                read_json_file(fp)
            elif lower.endswith('.csv'):
                read_csv_file(fp)

        return entries

    def aggregate_daily(  # type: ignore[override]
        self,
        entries: List['UsageEntry'],
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None
    ) -> List[Dict[str, Any]]:
        """Main aggregation method that reads data and returns aggregated results.
        Returns:
            List of aggregated data based on aggregation_mode
        """
        # This method serves dual purpose due to the provided skeleton:
        # - If entries are provided, aggregate them daily (or monthly based on mode).
        # - If entries are empty, read from data_path and aggregate according to aggregation_mode.
        src_entries: List[Dict[str, Any]] = []
        if entries:
            src_entries = [self._entry_to_dict(e) for e in entries]
        else:
            src_entries = self._read_entries_from_path()

        if self.aggregation_mode == 'monthly':
            return self._aggregate_by_period(
                src_entries,
                lambda d: d.strftime('%Y-%m'),
                'month',
                start_date,
                end_date
            )
        # Default daily
        return self._aggregate_by_period(
            src_entries,
            lambda d: d.strftime('%Y-%m-%d'),
            'date',
            start_date,
            end_date
        )
