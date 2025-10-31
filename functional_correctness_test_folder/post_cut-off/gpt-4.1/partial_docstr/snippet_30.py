
from dataclasses import dataclass, field
from typing import Dict, Any
from collections import defaultdict


class UsageEntry:
    def __init__(self, user: str, usage: float):
        self.user = user
        self.usage = usage


@dataclass
class AggregatedStats:
    '''Statistics for aggregated usage data.'''
    total_usage: float = 0.0
    entry_count: int = 0
    per_user: Dict[str, float] = field(
        default_factory=lambda: defaultdict(float))

    def add_entry(self, entry: UsageEntry) -> None:
        self.total_usage += entry.usage
        self.entry_count += 1
        self.per_user[entry.user] += entry.usage

    def to_dict(self) -> Dict[str, Any]:
        return {
            "total_usage": self.total_usage,
            "entry_count": self.entry_count,
            "per_user": dict(self.per_user)
        }
