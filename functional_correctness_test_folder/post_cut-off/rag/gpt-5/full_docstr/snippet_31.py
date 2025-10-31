from typing import Any, Callable, Dict, List, Optional, Iterable
from datetime import datetime
from collections import defaultdict
from zoneinfo import ZoneInfo
import os
import json
import csv
import numbers


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
        try:
            self.tz = ZoneInfo(timezone)
        except Exception:
            self.tz = ZoneInfo('UTC')

    def _parse_timestamp(self, ts: Any) -> Optional[datetime]:
        if ts is None:
            return None
        if isinstance(ts, datetime):
            return ts
        if isinstance(ts, (int, float)):
            # assume unix seconds if reasonable
            try:
                return datetime.fromtimestamp(ts)
            except Exception:
                return None
        if isinstance(ts, str):
            # try multiple formats
            fmts = [
                '%Y-%m-%dT%H:%M:%S.%fZ',
                '%Y-%m-%dT%H:%M:%SZ',
                '%Y-%m-%d %H:%M:%S',
                '%Y-%m-%d',
                '%m/%d/%Y %H:%M:%S',
                '%m/%d/%Y',
            ]
            for f in fmts:
                try:
                    return datetime.strptime(ts, f)
                except Exception:
                    continue
            # try fromisoformat
            try:
                return datetime.fromisoformat(ts.replace('Z', '+00:00'))
            except Exception:
                return None
        return None

    def _get_entry_timestamp(self, entry: Any) -> Optional[datetime]:
        # Try common timestamp field names
        candidates: Iterable[str] = (
            'timestamp', 'time', 'created_at', 'created', 'start', 'start_time', 'ts', 'date'
        )
        if isinstance(entry, dict):
            for k in candidates:
                if k in entry:
                    return self._parse_timestamp(entry.get(k))
        else:
            for k in candidates:
                if hasattr(entry, k):
                    return self._parse_timestamp(getattr(entry, k))
        return None

    def _coerce_tz(self, dt: datetime) -> datetime:
        if dt.tzinfo is None:
            return dt.replace(tzinfo=self.tz)
        try:
            return dt.astimezone(self.tz)
        except Exception:
            return dt

    def _should_include(self, dt: datetime, start_date: Optional[datetime], end_date: Optional[datetime]) -> bool:
        if start_date:
            if dt < start_date:
                return False
        if end_date:
            if dt > end_date:
                return False
        return True

    def _numeric_items(self, entry: Any) -> Dict[str, float]:
        out: Dict[str, float] = {}
        ignore = {'timestamp', 'time', 'created_at',
                  'created', 'start', 'start_time', 'ts', 'date'}
        data: Dict[str, Any]
        if isinstance(entry, dict):
            data = entry
        else:
            # extract __dict__ or use dir()
            try:
                data = {k: getattr(entry, k)
                        for k in dir(entry) if not k.startswith('_')}
            except Exception:
                data = {}
        for k, v in data.items():
            if k in ignore:
                continue
            if isinstance(v, bool):
                # treat bool as numeric only if explicitly included, default skip
                continue
            if isinstance(v, numbers.Number):
                out[k] = float(v)
        return out

    def _extract_user(self, entry: Any) -> Optional[str]:
        keys = ('user', 'user_id', 'userid', 'email', 'username')
        if isinstance(entry, dict):
            for k in keys:
                if k in entry and entry[k] is not None:
                    return str(entry[k])
        else:
            for k in keys:
                if hasattr(entry, k):
                    val = getattr(entry, k)
                    if val is not None:
                        return str(val)
        return None

    def _aggregate_by_period(self, entries: List[UsageEntry], period_key_func: Callable[[datetime], str], period_type: str, start_date: Optional[datetime] = None, end_date: Optional[datetime] = None) -> List[Dict[str, Any]]:
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
        groups: Dict[str, Dict[str, Any]] = {}
        users_per_period: Dict[str, set] = defaultdict(set)

        # normalize date filters to timezone
        sdt = self._coerce_tz(start_date) if isinstance(
            start_date, datetime) else None
        edt = self._coerce_tz(end_date) if isinstance(
            end_date, datetime) else None

        for entry in entries or []:
            ts = self._get_entry_timestamp(entry)
            if ts is None:
                continue
            ts = self._coerce_tz(ts)
            if not self._should_include(ts, sdt, edt):
                continue
            key = period_key_func(ts)
            agg = groups.get(key)
            if agg is None:
                agg = {period_type: key, 'count': 0}
                groups[key] = agg
            agg['count'] += 1

            # sum numeric fields by name
            metrics = self._numeric_items(entry)
            for mkey, mval in metrics.items():
                agg[mkey] = agg.get(mkey, 0.0) + mval

            user = self._extract_user(entry)
            if user:
                users_per_period[key].add(user)

        # finalize
        results: List[Dict[str, Any]] = []
        for key, agg in groups.items():
            agg['unique_users'] = len(users_per_period.get(key, set()))
            results.append(agg)

        # sort chronologically by parsed period
        def sort_key(rec: Dict[str, Any]) -> Any:
            val = rec.get(period_type)
            if period_type == 'date':
                # parse %Y-%m-%d
                try:
                    return datetime.strptime(str(val), '%Y-%m-%d')
                except Exception:
                    return str(val)
            else:
                try:
                    return datetime.strptime(str(val), '%Y-%m')
                except Exception:
                    return str(val)

        results.sort(key=sort_key)
        return results

    def aggregate_daily(self, entries: List[UsageEntry], start_date: Optional[datetime] = None, end_date: Optional[datetime] = None) -> List[Dict[str, Any]]:
        '''Aggregate usage data by day.
        Args:
            entries: List of usage entries
            start_date: Optional start date filter
            end_date: Optional end date filter
        Returns:
            List of daily aggregated data
        '''
        def day_key(dt: datetime) -> str:
            dt = self._coerce_tz(dt)
            return dt.strftime('%Y-%m-%d')

        return self._aggregate_by_period(entries, day_key, 'date', start_date, end_date)

    def aggregate_monthly(self, entries: List[UsageEntry], start_date: Optional[datetime] = None, end_date: Optional[datetime] = None) -> List[Dict[str, Any]]:
        '''Aggregate usage data by month.
        Args:
            entries: List of usage entries
            start_date: Optional start date filter
            end_date: Optional end date filter
        Returns:
            List of monthly aggregated data
        '''
        def month_key(dt: datetime) -> str:
            dt = self._coerce_tz(dt)
            return dt.strftime('%Y-%m')

        return self._aggregate_by_period(entries, month_key, 'month', start_date, end_date)

    def aggregate_from_blocks(self, blocks: List[SessionBlock], view_type: str = 'daily') -> List[Dict[str, Any]]:
        '''Aggregate data from session blocks.
        Args:
            blocks: List of session blocks
            view_type: Type of aggregation ('daily' or 'monthly')
        Returns:
            List of aggregated data
        '''
        entries: List[Any] = []
        for b in blocks or []:
            # Handle dict-like blocks
            if isinstance(b, dict):
                if 'entries' in b and isinstance(b['entries'], list):
                    entries.extend(b['entries'])
                elif 'usage' in b and isinstance(b['usage'], list):
                    entries.extend(b['usage'])
                elif 'records' in b and isinstance(b['records'], list):
                    entries.extend(b['records'])
                else:
                    # treat as one entry
                    entries.append(b)
            else:
                # object-like blocks
                if hasattr(b, 'entries') and isinstance(getattr(b, 'entries'), list):
                    entries.extend(getattr(b, 'entries'))
                elif hasattr(b, 'usage') and isinstance(getattr(b, 'usage'), list):
                    entries.extend(getattr(b, 'usage'))
                else:
                    entries.append(b)

        if view_type == 'monthly':
            return self.aggregate_monthly(entries)
        return self.aggregate_daily(entries)

    def calculate_totals(self, aggregated_data: List[Dict[str, Any]]) -> Dict[str, Any]:
        '''Calculate totals from aggregated data.
        Args:
            aggregated_data: List of aggregated daily or monthly data
        Returns:
            Dictionary with total statistics
        '''
        totals: Dict[str, Any] = {'periods': len(aggregated_data or [])}
        numeric_keys: set = set()
        for rec in aggregated_data or []:
            for k, v in rec.items():
                if k in ('date', 'month'):
                    continue
                if isinstance(v, bool):
                    continue
                if isinstance(v, numbers.Number):
                    numeric_keys.add(k)
        for k in numeric_keys:
            totals[k] = 0.0
        for rec in aggregated_data or []:
            for k in numeric_keys:
                v = rec.get(k, 0.0)
                if isinstance(v, numbers.Number) and not isinstance(v, bool):
                    totals[k] += float(v)
        return totals

    def _read_entries_from_path(self) -> List[Dict[str, Any]]:
        entries: List[Dict[str, Any]] = []
        if not self.data_path or not os.path.exists(self.data_path):
            return entries

        def _read_json_file(fp: str):
            try:
                with open(fp, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                if isinstance(data, list):
                    return data
                if isinstance(data, dict):
                    if 'entries' in data and isinstance(data['entries'], list):
                        return data['entries']
                    if 'data' in data and isinstance(data['data'], list):
                        return data['data']
                    return [data]
            except Exception:
                return []

        def _read_jsonl_file(fp: str):
            out = []
            try:
                with open(fp, 'r', encoding='utf-8') as f:
                    for line in f:
                        line = line.strip()
                        if not line:
                            continue
                        try:
                            out.append(json.loads(line))
                        except Exception:
                            continue
            except Exception:
                return []
            return out

        def _read_csv_file(fp: str):
            out = []
            try:
                with open(fp, 'r', encoding='utf-8') as f:
                    reader = csv.DictReader(f)
                    for row in reader:
                        out.append(row)
            except Exception:
                return []
            return out

        if os.path.isdir(self.data_path):
            for root, _, files in os.walk(self.data_path):
                for name in files:
                    path = os.path.join(root, name)
                    lower = name.lower()
                    if lower.endswith('.json'):
                        entries.extend(_read_json_file(path))
                    elif lower.endswith('.jsonl') or lower.endswith('.ndjson'):
                        entries.extend(_read_jsonl_file(path))
                    elif lower.endswith('.csv'):
                        entries.extend(_read_csv_file(path))
        else:
            lower = self.data_path.lower()
            if lower.endswith('.json'):
                entries.extend(_read_json_file(self.data_path))
            elif lower.endswith('.jsonl') or lower.endswith('.ndjson'):
                entries.extend(_read_jsonl_file(self.data_path))
            elif lower.endswith('.csv'):
                entries.extend(_read_csv_file(self.data_path))

        return entries

    def aggregate_daily(self, entries: List[UsageEntry], start_date: Optional[datetime] = None, end_date: Optional[datetime] = None) -> List[Dict[str, Any]]:
        '''Main aggregation method that reads data and returns aggregated results.
        Returns:
            List of aggregated data based on aggregation_mode
        '''
        # If entries are provided, behave as daily aggregator using provided data.
        if entries:
            if self.aggregation_mode == 'monthly':
                return self.aggregate_monthly(entries, start_date, end_date)
            return self._aggregate_by_period(
                entries,
                lambda dt: self._coerce_tz(dt).strftime('%Y-%m-%d'),
                'date',
                start_date,
                end_date,
            )

        # Otherwise, read from data_path and aggregate.
        loaded_entries = self._read_entries_from_path()
        if self.aggregation_mode == 'monthly':
            return self.aggregate_monthly(loaded_entries, start_date, end_date)
        return self._aggregate_by_period(
            loaded_entries,
            lambda dt: self._coerce_tz(dt).strftime('%Y-%m-%d'),
            'date',
            start_date,
            end_date,
        )
