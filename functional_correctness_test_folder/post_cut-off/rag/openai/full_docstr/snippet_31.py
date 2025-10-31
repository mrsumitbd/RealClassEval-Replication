
import json
import os
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Any, Callable, Dict, Iterable, List, Optional, Tuple

# --------------------------------------------------------------------------- #
# Simple data structures used by the aggregator
# --------------------------------------------------------------------------- #


@dataclass
class UsageEntry:
    """Represents a single usage record."""
    timestamp: datetime
    value: float

    @staticmethod
    def from_dict(d: Dict[str, Any]) -> "UsageEntry":
        """Create a UsageEntry from a dictionary."""
        ts = d.get("timestamp") or d.get("time") or d.get("datetime")
        if isinstance(ts, str):
            ts = datetime.fromisoformat(ts)
        elif not isinstance(ts, datetime):
            raise ValueError(f"Unsupported timestamp type: {ts!r}")
        val = d.get("value") or d.get("usage") or d.get("amount") or 0.0
        return UsageEntry(timestamp=ts, value=float(val))


@dataclass
class SessionBlock:
    """Represents a block of usage entries."""
    entries: List[UsageEntry]

    @staticmethod
    def from_file(path: Path) -> "SessionBlock":
        """Read a block from a JSON file containing a list of entries."""
        with path.open("r", encoding="utf-8") as f:
            data = json.load(f)
        if not isinstance(data, list):
            raise ValueError(f"Expected a list of entries in {path}")
        entries = [UsageEntry.from_dict(d) for d in data]
        return SessionBlock(entries=entries)


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
        agg: Dict[str, float] = {}
        for e in filtered:
            key = period_key_func(e.timestamp)
            agg[key] = agg.get(key, 0.0) + e.value

        # Build result list
        result: List[Dict[str, Any]] = []
        for key, total in sorted(agg.items()):
            result.append(
                {
                    period_type: key,
                    "total": total,
                }
            )
        return result

    # --------------------------------------------------------------------- #
    # Specific aggregation methods
    # --------------------------------------------------------------------- #

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

    # --------------------------------------------------------------------- #
    # Aggregation from raw blocks
    # --------------------------------------------------------------------- #

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

    # --------------------------------------------------------------------- #
    # Totals calculation
    # --------------------------------------------------------------------- #

    def calculate_totals(self, aggregated_data: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Calculate totals from aggregated data.

        Args:
            aggregated_data: List of aggregated daily or monthly data

        Returns:
            Dictionary with total statistics
        """
        total = sum(item.get("total", 0.0) for item in aggregated_data)
        count = len(aggregated_data)
        avg = total / count if count else 0.0
        return {"total": total, "count": count, "average": avg}

    # --------------------------------------------------------------------- #
    # Main aggregation entry point
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
        # Load all blocks from the data directory
        blocks: List[SessionBlock] = []
        for path in self.data_path.glob("*"):
            if path.is_file():
                try:
                    blocks.append(SessionBlock.from_file(path))
                except Exception:
                    # Skip files that cannot be parsed
                    continue

        # Aggregate according to the configured mode
        if self.aggregation_mode == "daily":
            return self.aggregate_from_blocks(blocks, view_type="daily")
        else:
            return self.aggregate_from_blocks(blocks, view_type="monthly")
