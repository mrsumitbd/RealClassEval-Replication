
from dataclasses import dataclass, field
from typing import Dict, Any


@dataclass
class AggregatedStats:
    """Statistics for aggregated usage data."""
    total_runs: int = 0
    total_pipettes_used: int = 0
    total_modules_used: int = 0
    total_protocol_runs: int = 0
    total_labs: int = field(default=0)
    pipette_usage_by_model: Dict[str, int] = field(default_factory=dict)
    module_usage_by_model: Dict[str, int] = field(default_factory=dict)

    def add_entry(self, entry: 'UsageEntry') -> None:
        """Add an entry's statistics to this aggregate."""
        self.total_runs += entry.total_runs
        self.total_pipettes_used += entry.total_pipettes_used
        self.total_modules_used += entry.total_modules_used
        self.total_protocol_runs += entry.total_protocol_runs
        self.total_labs += entry.total_labs
        for model, count in entry.pipette_usage_by_model.items():
            self.pipette_usage_by_model[model] = self.pipette_usage_by_model.get(
                model, 0) + count
        for model, count in entry.module_usage_by_model.items():
            self.module_usage_by_model[model] = self.module_usage_by_model.get(
                model, 0) + count

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary format."""
        return {
            'total_runs': self.total_runs,
            'total_pipettes_used': self.total_pipettes_used,
            'total_modules_used': self.total_modules_used,
            'total_protocol_runs': self.total_protocol_runs,
            'total_labs': self.total_labs,
            'pipette_usage_by_model': self.pipette_usage_by_model,
            'module_usage_by_model': self.module_usage_by_model,
        }
