
from dataclasses import dataclass, field
from typing import Dict, Any
from collections import defaultdict


@dataclass
class UsageEntry:
    category: str
    value: float


@dataclass
class AggregatedStats:
    totals: Dict[str, float] = field(
        default_factory=lambda: defaultdict(float))
    count: Dict[str, int] = field(default_factory=lambda: defaultdict(int))

    def add_entry(self, entry: UsageEntry) -> None:
        self.totals[entry.category] += entry.value
        self.count[entry.category] += 1

    def to_dict(self) -> Dict[str, Any]:
        return {
            category: {
                "total": self.totals[category],
                "count": self.count[category]
            }
            for category in self.totals
        }
