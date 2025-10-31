
import json
import os
from datetime import datetime
from pathlib import Path
from typing import Any, Callable, Dict, Iterable, List, Optional, Tuple

try:
    from dateutil import tz
except Exception:  # pragma: no cover
    tz = None  # type: ignore


# --------------------------------------------------------------------------- #
# Simple data structures used by the aggregator
# --------------------------------------------------------------------------- #
class UsageEntry:
    """Represents a single usage record."""

    def __init__(self, timestamp: datetime, metrics: Dict[str, float]):
        self.timestamp = timestamp
        self.metrics = metrics

    @classmethod
    def from_dict(cls, d: Dict[str, Any]) -> "UsageEntry":
        ts = d.get("timestamp")
        if isinstance(ts, str):
            ts = datetime.fromisoformat(ts)
        elif not isinstance(ts, datetime):
            raise ValueError("timestamp must be a datetime or ISO string")
        metrics = {k: float(v) for k, v in d.items() if k != "timestamp"}
        return cls(ts, metrics)


class SessionBlock:
    """Container for a batch of usage entries."""

    def __init__(self, entries: List[UsageEntry]):
        self.entries = entries

    @classmethod
    def from_dict(cls, d: Dict[str, Any]) -> "SessionBlock":
        entries = [UsageEntry.from_dict(e) for e in d.get("entries", [])]
        return cls(entries)


# --------------------------------------------------------------------------- #
# The aggregator implementation
# --------------------------------------------------------------------------- #
class UsageAggregator:
    """Aggregates usage data for daily and monthly reports."""

    def __init__(self, data_path: str, aggregation_mode: str = "daily", timezone: str = "UTC"):
        """
        Initialize the aggregator.

        Args:
            data_path: Path to the data directory
            aggregation_mode: Mode of aggregation ('daily' or 'monthly')
            timezone: Timezone string for date formatting
        """
        self.data_path = Path(data_path)
        if aggregation_mode not in {"daily", "monthly"}:
            raise ValueError("aggregation_mode must be 'daily' or 'monthly'")
        self.aggregation_mode = aggregation_mode
        self.timezone = timezone

    # --------------------------------------------------------------------- #
    # Generic aggregation helpers
    # --------------------------------------------------------------------- #
    def _aggregate_by_period(
        self,
        entries: List[UsageEntry],
        period_key_func: Callable[[datetime], str],
        period_type: str,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None,
    ) -> List[Dict[str, Any]]:
        """
        Generic aggregation by time period.

        Args:
            entries: List of usage entries
            period_key_func: Function to extract period key from timestamp
            period_type: Type of period ('date' or 'month')
            start_date: Optional start date filter
            end_date: Optional end date filter

        Returns:
            List of aggregated data dictionaries
        """
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
        agg: Dict[str, Dict[str, float]] = {}
        for e in filtered:
            key = period_key_func(e.timestamp)
            if key not in agg:
                agg[key] = {}
            for k, v in e.metrics.items():
                agg[key][k] = agg[key].get(k, 0.0) + v

        # Build result list
        result: List[Dict[str, Any]] = []
        for key, metrics in sorted(agg.items()):
            row: Dict[str, Any] = {"period": key}
            row.update(metrics)
            result.append(row)
        return result

    # --------------------------------------------------------------------- #
    # Public aggregation methods
    # --------------------------------------------------------------------- #
    def aggregate_daily(
        self,
        entries: List[UsageEntry],
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None,
    ) -> List[Dict[str, Any]]:
        """Aggregate usage data by day."""

        def key_func(ts): return ts.astimezone(
            tz.gettz(self.timezone)).strftime("%Y-%m-%d")
        return self._aggregate_by_period(entries, key_func, "date", start_date, end_date)

    def aggregate_monthly(
        self,
        entries: List[UsageEntry],
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None,
    ) -> List[Dict[str, Any]]:
        """Aggregate usage data by month."""

        def key_func(ts): return ts.astimezone(
            tz.gettz(self.timezone)).strftime("%Y-%m")
        return self._aggregate_by_period(entries, key_func, "month", start_date, end_date)

    def aggregate_from_blocks(
        self,
        blocks: List[SessionBlock],
        view_type: str = "daily",
    ) -> List[Dict[str, Any]]:
        """Aggregate data from session blocks."""
        all_entries: List[UsageEntry] = []
        for block in blocks:
            all_entries.extend(block.entries)
        if view_type == "daily":
            return self.aggregate_daily(all_entries)
        elif view_type == "monthly":
            return self.aggregate_monthly(all_entries)
        else:
            raise ValueError("view_type must be 'daily' or 'monthly'")

    def calculate_totals(
        self,
        aggregated_data: List[Dict[str, Any]],
    ) -> Dict[str, Any]:
        """Calculate totals from aggregated data."""
        totals: Dict[str, float] = {}
        for row in aggregated_data:
            for k, v in row.items():
                if k == "period":
                    continue
                totals[k] = totals.get(k, 0.0) + v
        return totals

    # --------------------------------------------------------------------- #
    # Main entry point
    # --------------------------------------------------------------------- #
    def aggregate_daily(
        self,
        entries: List[UsageEntry],
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None,
    ) -> List[Dict[str, Any]]:
        """
        Main aggregation method that reads data and returns aggregated results.
        Returns:
            List of aggregated data based on aggregation_mode
        """
        # Load entries from data_path if entries not provided
        if not entries:
            entries = self._load_entries_from_path()

        if self.aggregation_mode == "daily":
            return self.aggregate_daily(entries, start_date, end_date)
        else:
            return self.aggregate_monthly(entries, start_date, end_date)

    # --------------------------------------------------------------------- #
    # Helper to load entries from the data directory
    # --------------------------------------------------------------------- #
    def _load_entries_from_path(self) -> List[UsageEntry]:
        """Load usage entries from JSON files in the data directory."""
        entries: List[UsageEntry] = []
        if not self.data_path.exists():
            return entries
        for p in self.data_path.rglob("*.json"):
            try:
                with p.open("r", encoding="utf-8") as f:
                    data = json.load(f)
                if isinstance(data, list):
                    for d in data:
                        entries.append(UsageEntry.from_dict(d))
                elif isinstance(data, dict):
                    entries.append(UsageEntry.from_dict(data))
            except Exception:
                # Skip files that cannot be parsed
                continue
        return entries
