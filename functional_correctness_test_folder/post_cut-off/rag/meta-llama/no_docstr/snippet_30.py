
from dataclasses import dataclass, field
from typing import Dict, Any


@dataclass
class AggregatedStats:
    """Statistics for aggregated usage data."""
    total_usage_time: float = field(default=0.0)
    total_runs: int = field(default=0)
    total_pipettes_used: int = field(default=0)
    total_modules_used: int = field(default=0)
    pipette_usage_times: Dict[str, float] = field(default_factory=dict)
    module_usage_times: Dict[str, float] = field(default_factory=dict)

    def add_entry(self, entry: 'UsageEntry') -> None:
        """Add an entry's statistics to this aggregate."""
        self.total_usage_time += entry.total_usage_time
        self.total_runs += entry.total_runs
        self.total_pipettes_used += entry.total_pipettes_used
        self.total_modules_used += entry.total_modules_used
        for pipette_id, usage_time in entry.pipette_usage_times.items():
            self.pipette_usage_times[pipette_id] = self.pipette_usage_times.get(
                pipette_id, 0) + usage_time
        for module_id, usage_time in entry.module_usage_times.items():
            self.module_usage_times[module_id] = self.module_usage_times.get(
                module_id, 0) + usage_time

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary format."""
        return {
            'total_usage_time': self.total_usage_time,
            'total_runs': self.total_runs,
            'total_pipettes_used': self.total_pipettes_used,
            'total_modules_used': self.total_modules_used,
            'pipette_usage_times': self.pipette_usage_times,
            'module_usage_times': self.module_usage_times
        }
