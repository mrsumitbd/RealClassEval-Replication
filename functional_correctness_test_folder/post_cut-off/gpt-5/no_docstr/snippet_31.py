from __future__ import annotations

from typing import Any, Callable, Dict, List, Optional
from datetime import datetime, timedelta, timezone as dt_timezone
from zoneinfo import ZoneInfo


class UsageAggregator:
    def __init__(self, data_path: str, aggregation_mode: str = 'daily', timezone: str = 'UTC'):
        self.data_path = data_path
        self.aggregation_mode = aggregation_mode
        try:
            self.tz = ZoneInfo(timezone)
        except Exception:
            self.tz = dt_timezone.utc
        self._default_daily_fmt = "%Y-%m-%d"
        self._default_monthly_fmt = "%Y-%m"

    # Utility helpers

    def _get_attr(self, obj: Any, names: List[str], default: Any = None) -> Any:
        # Support both dict-like and attribute-like access
        for n in names:
            if isinstance(obj, dict) and n in obj:
                return obj[n]
            if hasattr(obj, n):
                return getattr(obj, n)
        return default

    def _ensure_tz(self, dt: Optional[datetime]) -> Optional[datetime]:
        if dt is None:
            return None
        if dt.tzinfo is None:
            return dt.replace(tzinfo=self.tz)
        try:
            # Convert to target tz
            return dt.astimezone(self.tz)
        except Exception:
            return dt

    def _entry_timestamp(self, entry: Any) -> Optional[datetime]:
        dt = self._get_attr(
            entry, ["timestamp", "time", "date", "start", "start_time"])
        dt = self._ensure_tz(dt)
        return dt

    def _entry_duration_seconds(self, entry: Any) -> float:
        # Priority: explicit duration, else end-start if both available, else 0
        dur = self._get_attr(
            entry, ["duration", "duration_seconds", "seconds", "secs"])
        if isinstance(dur, (int, float)) and dur >= 0:
            return float(dur)
        start = self._get_attr(entry, ["start", "start_time"])
        end = self._get_attr(entry, ["end", "end_time", "stop"])
        start = self._ensure_tz(start) if isinstance(start, datetime) else None
        end = self._ensure_tz(end) if isinstance(end, datetime) else None
        if isinstance(start, datetime) and isinstance(end, datetime):
            delta = (end - start).total_seconds()
            return float(delta) if delta >= 0 else 0.0
        return 0.0

    def _entry_quantity(self, entry: Any) -> float:
        # Try common quantity fields and fall back to 0
        for name in ["quantity", "amount", "usage", "value", "data_used", "bytes", "units"]:
            val = self._get_attr(entry, [name])
            if isinstance(val, (int, float)):
                return float(val)
        return 0.0

    def _period_key_daily(self, dt: datetime) -> str:
        return dt.strftime(self._default_daily_fmt)

    def _period_key_monthly(self, dt: datetime) -> str:
        return dt.strftime(self._default_monthly_fmt)

    def _period_bounds(self, key: str, period_type: str) -> (datetime, datetime):
        if period_type == "day":
            start = datetime.strptime(
                key, self._default_daily_fmt).replace(tzinfo=self.tz)
            end = start + timedelta(days=1)
            return start, end
        if period_type == "month":
            dt_month = datetime.strptime(
                key, self._default_monthly_fmt).replace(tzinfo=self.tz)
            year = dt_month.year
            month = dt_month.month
            if month == 12:
                next_month = datetime(
                    year=year + 1, month=1, day=1, tzinfo=self.tz)
            else:
                next_month = datetime(
                    year=year, month=month + 1, day=1, tzinfo=self.tz)
            return dt_month, next_month
        # Fallback: treat as instant
        start = datetime.fromisoformat(key).replace(
            tzinfo=self.tz) if key else datetime.now(self.tz)
        return start, start

    def _filter_by_date(
        self,
        entries: List[Any],
        start_date: Optional[datetime],
        end_date: Optional[datetime],
    ) -> List[Any]:
        s = self._ensure_tz(start_date)
        e = self._ensure_tz(end_date)
        out: List[Any] = []
        for entry in entries:
            ts = self._entry_timestamp(entry)
            if ts is None:
                continue
            if s and ts < s:
                continue
            if e and ts > e:
                continue
            out.append(entry)
        return out

    def _aggregate_by_period(
        self,
        entries: List[Any],
        period_key_func: Callable[[datetime], str],
        period_type: str,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None,
    ) -> List[Dict[str, Any]]:
        if not entries:
            return []

        filtered = self._filter_by_date(entries, start_date, end_date)
        if not filtered:
            return []

        buckets: Dict[str, Dict[str, Any]] = {}

        for entry in filtered:
            ts = self._entry_timestamp(entry)
            if ts is None:
                continue
            key = period_key_func(ts)
            bucket = buckets.get(key)
            if bucket is None:
                p_start, p_end = self._period_bounds(key, period_type)
                bucket = {
                    "period": key,
                    "period_type": period_type,
                    "start": p_start,
                    "end": p_end,
                    "count": 0,
                    "total_duration": 0.0,
                    "total_quantity": 0.0,
                    "items": [],
                }
                buckets[key] = bucket

            bucket["count"] += 1
            bucket["total_duration"] += float(
                self._entry_duration_seconds(entry))
            bucket["total_quantity"] += float(self._entry_quantity(entry))
            bucket["items"].append(entry)

        # Sort by period start
        result = sorted(buckets.values(), key=lambda x: x["start"])
        return result

    def aggregate_daily(
        self,
        entries: List[Any],
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None,
    ) -> List[Dict[str, Any]]:
        # This definition is shadowed by the later one in the class; kept to match the skeleton.
        return self._aggregate_by_period(entries, self._period_key_daily, "day", start_date, end_date)

    def aggregate_monthly(
        self,
        entries: List[Any],
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None,
    ) -> List[Dict[str, Any]]:
        return self._aggregate_by_period(entries, self._period_key_monthly, "month", start_date, end_date)

    def aggregate_from_blocks(self, blocks: List[Any], view_type: str = 'daily') -> List[Dict[str, Any]]:
        if not blocks:
            return []
        entries: List[Dict[str, Any]] = []
        for b in blocks:
            start = self._get_attr(b, ["start", "start_time"])
            end = self._get_attr(b, ["end", "end_time", "stop"])
            ts = self._ensure_tz(start) if isinstance(
                start, datetime) else None
            duration = 0.0
            if isinstance(start, datetime) and isinstance(end, datetime):
                start_tz = self._ensure_tz(start)
                end_tz = self._ensure_tz(end)
                duration = max(0.0, (end_tz - start_tz).total_seconds())
            quantity = self._entry_quantity(b)
            entries.append(
                {
                    "timestamp": ts,
                    "start": self._ensure_tz(start) if isinstance(start, datetime) else None,
                    "end": self._ensure_tz(end) if isinstance(end, datetime) else None,
                    "duration": duration,
                    "quantity": quantity,
                    "original": b,
                }
            )

        if view_type == 'monthly':
            return self.aggregate_monthly(entries)
        # default to daily
        return self.aggregate_daily(entries)

    def calculate_totals(self, aggregated_data: List[Dict[str, Any]]) -> Dict[str, Any]:
        if not aggregated_data:
            return {
                "periods": 0,
                "total_count": 0,
                "total_duration": 0.0,
                "total_quantity": 0.0,
                "start": None,
                "end": None,
            }
        total_count = sum(d.get("count", 0) for d in aggregated_data)
        total_duration = sum(float(d.get("total_duration", 0.0))
                             for d in aggregated_data)
        total_quantity = sum(float(d.get("total_quantity", 0.0))
                             for d in aggregated_data)
        starts = [d.get("start") for d in aggregated_data if isinstance(
            d.get("start"), datetime)]
        ends = [d.get("end")
                for d in aggregated_data if isinstance(d.get("end"), datetime)]
        return {
            "periods": len(aggregated_data),
            "total_count": total_count,
            "total_duration": total_duration,
            "total_quantity": total_quantity,
            "start": min(starts) if starts else None,
            "end": max(ends) if ends else None,
        }

    def aggregate_daily(
        self,
        entries: List[Any],
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None,
    ) -> List[Dict[str, Any]]:
        return self._aggregate_by_period(entries, self._period_key_daily, "day", start_date, end_date)
