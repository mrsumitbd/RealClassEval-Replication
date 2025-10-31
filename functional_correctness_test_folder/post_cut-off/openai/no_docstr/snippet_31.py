
from __future__ import annotations

from datetime import datetime
from typing import Any, Callable, Dict, List, Optional

# Minimal placeholder types for UsageEntry and SessionBlock
# In real usage these would be imported from the actual data model.


class UsageEntry:
    def __init__(self, timestamp: datetime, usage: float):
        self.timestamp = timestamp
        self.usage = usage


class SessionBlock:
    def __init__(self, start_time: datetime, end_time: datetime, usage: float):
        self.start_time = start_time
        self.end_time = end_time
        self.usage = usage


class UsageAggregator:
    def __init__(self, data_path: str, aggregation_mode: str = 'daily', timezone: str = 'UTC'):
        self.data_path = data_path
        self.aggregation_mode = aggregation_mode
        self.timezone = timezone

    def _aggregate_by_period(
        self,
        entries: List[UsageEntry],
        period_key_func: Callable[[datetime], str],
        period_type: str,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None,
    ) -> List[Dict[str, Any]]:
        # Filter entries by date range if provided
        filtered = []
        for entry in entries:
            ts = entry.timestamp
            if start_date and ts < start_date:
                continue
            if end_date and ts > end_date:
                continue
            filtered.append(entry)

        # Group by period key
        agg: Dict[str, Dict[str, Any]] = {}
        for entry in filtered:
            key = period_key_func(entry.timestamp)
            if key not in agg:
                agg[key] = {
                    'period': key,
                    'total_usage': 0.0,
                    'count': 0,
                }
            agg[key]['total_usage'] += entry.usage
            agg[key]['count'] += 1

        # Convert to list and sort by period
        result = list(agg.values())
        result.sort(key=lambda x: x['period'])
        return result

    def aggregate_daily(
        self,
        entries: List[UsageEntry],
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None,
    ) -> List[Dict[str, Any]]:
        return self._aggregate_by_period(
            entries,
            period_key_func=lambda dt: dt.strftime('%Y-%m-%d'),
            period_type='daily',
            start_date=start_date,
            end_date=end_date,
        )

    def aggregate_monthly(
        self,
        entries: List[UsageEntry],
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None,
    ) -> List[Dict[str, Any]]:
        return self._aggregate_by_period(
            entries,
            period_key_func=lambda dt: dt.strftime('%Y-%m'),
            period_type='monthly',
            start_date=start_date,
            end_date=end_date,
        )

    def aggregate_from_blocks(
        self,
        blocks: List[SessionBlock],
        view_type: str = 'daily',
    ) -> List[Dict[str, Any]]:
        # Convert blocks to entries using the block start time as the timestamp
        entries: List[UsageEntry] = [
            UsageEntry(timestamp=block.start_time, usage=block.usage) for block in blocks
        ]
        if view_type == 'daily':
            return self.aggregate_daily(entries)
        elif view_type == 'monthly':
            return self.aggregate_monthly(entries)
        else:
            raise ValueError(f"Unsupported view_type: {view_type}")

    def calculate_totals(self, aggregated_data: List[Dict[str, Any]]) -> Dict[str, Any]:
        total_usage = sum(item['total_usage'] for item in aggregated_data)
        total_count = sum(item['count'] for item in aggregated_data)
        average_usage = total_usage / total_count if total_count else 0.0
        return {
            'total_usage': total_usage,
            'total_count': total_count,
            'average_usage': average_usage,
        }
