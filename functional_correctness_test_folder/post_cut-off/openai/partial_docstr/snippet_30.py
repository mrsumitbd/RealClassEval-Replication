
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict


@dataclass
class AggregatedStats:
    '''Statistics for aggregated usage data.'''
    total_entries: int = 0
    total_count: int = 0
    by_resource: Dict[str, int] = field(default_factory=dict)
    by_user: Dict[str, int] = field(default_factory=dict)

    def add_entry(self, entry: Any) -> None:
        """
        Add a usage entry to the aggregated statistics.

        The entry is expected to have the following optional attributes:
            - count (int): the amount to add to the total count. Defaults to 1.
            - resource (str): a key used to aggregate per-resource counts.
            - user_id (str): a key used to aggregate per-user counts.
        """
        # Increment the number of processed entries
        self.total_entries += 1

        # Determine the count value (default to 1 if not present)
        count = getattr(entry, "count", 1)
        if not isinstance(count, int):
            try:
                count = int(count)
            except Exception:
                count = 1
        self.total_count += count

        # Aggregate by resource if available
        resource = getattr(entry, "resource", None)
        if isinstance(resource, str):
            self.by_resource[resource] = self.by_resource.get(
                resource, 0) + count

        # Aggregate by user if available
        user = getattr(entry, "user_id", None)
        if isinstance(user, str):
            self.by_user[user] = self.by_user.get(user, 0) + count

    def to_dict(self) -> Dict[str, Any]:
        """Convert the aggregated statistics to a plain dictionary."""
        return {
            "total_entries": self.total_entries,
            "total_count": self.total_count,
            "by_resource": dict(self.by_resource),
            "by_user": dict(self.by_user),
        }
