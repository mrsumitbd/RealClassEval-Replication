
import json
import os
from datetime import datetime
from pathlib import Path
from typing import Any, Callable, Dict, Iterable, List, Optional

# --------------------------------------------------------------------------- #
# Helper data structures
# --------------------------------------------------------------------------- #


class UsageEntry:
    """Simple representation of a usage record."""

    def __init__(self, timestamp: datetime, usage: float, **extra: Any):
        self.timestamp = timestamp
        self.usage = usage
        self.extra = extra


class SessionBlock:
    """Container that holds a list of UsageEntry objects."""

    def __init__(self, entries: List[UsageEntry]):
        self.entries = entries

# --------------------------------------------------------------------------- #
# Main aggregator
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

    # ----------------------------------------------------------------------- #
    # Generic aggregation helper
    # ----------------------------------------------------------------------- #
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
        agg: Dict[str, float] = {}
        for e in filtered:
            key = period_key_func(e.timestamp)
            agg[key] = agg.get(key, 0.0) + e.usage

        # Build result list
        result: List[Dict[str, Any]] = []
        for key, total in sorted(agg.items()):
            result.append(
                {
                    period_type: key,
                    "total_usage": total,
                }
            )
        return result

    # ----------------------------------------------------------------------- #
    # Daily aggregation
    # ----------------------------------------------------------------------- #
    def aggregate_daily(
        self,
        entries: List[UsageEntry],
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None,
    ) -> List[Dict[str, Any]]:
        """
        Aggregate usage data by day.

        Args:
            entries: List of usage entries
            start_date: Optional start date filter
            end_date: Optional end date filter

        Returns:
            List of daily aggregated data
        """
        return self._aggregate_by_period(
            entries,
            period_key_func=lambda ts: ts.strftime("%Y-%m-%d"),
            period_type="date",
            start_date=start_date,
            end_date=end_date,
        )

    # ----------------------------------------------------------------------- #
    # Monthly aggregation
    # ----------------------------------------------------------------------- #
    def aggregate_monthly(
        self,
        entries: List[UsageEntry],
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None,
    ) -> List[Dict[str, Any]]:
        """
        Aggregate usage data by month.

        Args:
            entries: List of usage entries
            start_date: Optional start date filter
            end_date: Optional end date filter

        Returns:
            List of monthly aggregated data
        """
        return self._aggregate_by_period(
            entries,
            period_key_func=lambda ts: ts.strftime("%Y-%m"),
            period_type="month",
            start_date=start_date,
            end_date=end_date,
        )

    # ----------------------------------------------------------------------- #
    # Aggregation from session blocks
    # ----------------------------------------------------------------------- #
    def aggregate_from_blocks(
        self,
        blocks: List[SessionBlock],
        view_type: str = "daily",
    ) -> List[Dict[str, Any]]:
        """
        Aggregate data from session blocks.

        Args:
            blocks: List of session blocks
            view_type: Type of aggregation ('daily' or 'monthly')

        Returns:
            List of aggregated data
        """
        all_entries: List[UsageEntry] = []
        for block in blocks:
            all_entries.extend(block.entries)

        if view_type == "daily":
            return self.aggregate_daily(all_entries)
        elif view_type == "monthly":
            return self.aggregate_monthly(all_entries)
        else:
            raise ValueError("view_type must be 'daily' or 'monthly'")

    # ----------------------------------------------------------------------- #
    # Totals calculation
    # ----------------------------------------------------------------------- #
    def calculate_totals(self, aggregated_data: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Calculate totals from aggregated data.

        Args:
            aggregated_data: List of aggregated daily or monthly data

        Returns:
            Dictionary with total statistics
        """
        total_usage = sum(item.get("total_usage", 0.0)
                          for item in aggregated_data)
        count = len(aggregated_data)
        return {
            "total_usage": total_usage,
            "period_count": count,
            "average_per_period": total_usage / count if count else 0.0,
        }

    # ----------------------------------------------------------------------- #
    # Main aggregation method
    # ----------------------------------------------------------------------- #
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
        # Load data from data_path
        all_entries: List[UsageEntry] = []

        # Assume JSON Lines files in the directory
        for file_path in self.data_path.glob("*.jsonl"):
            with open(file_path, "r", encoding="utf-8") as f:
                for line in f:
                    if not line.strip():
                        continue
                    rec = json.loads(line)
                    ts_str = rec.get("timestamp")
                    if not ts_str:
                        continue
                    ts = datetime.fromisoformat(ts_str)
                    usage = float(rec.get("usage", 0.0))
                    all_entries.append(UsageEntry(
                        timestamp=ts, usage=usage, **rec))

        # Perform aggregation
        if self.aggregation_mode == "daily":
            agg = self.aggregate_daily(all_entries, start_date, end_date)
        else:
            agg = self.aggregate_monthly(all_entries, start_date, end_date)

        return agg
