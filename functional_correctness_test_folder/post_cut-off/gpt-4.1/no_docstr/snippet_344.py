
from dataclasses import dataclass, field
from typing import Any, Dict


@dataclass
class OptimizationResults:
    data: Dict[str, Any] = field(default_factory=dict)
    plotting_data: Dict[str, Any] = field(default_factory=dict)

    def __post_init__(self):
        if self.data is None:
            self.data = {}
        if self.plotting_data is None:
            self.plotting_data = {}

    def update_plotting_data(self, **kwargs):
        self.plotting_data.update(kwargs)

    def get(self, key: str, default: Any = None) -> Any:
        return self.data.get(key, default)

    def __getitem__(self, key: str) -> Any:
        return self.data[key]

    def __setitem__(self, key: str, value: Any):
        self.data[key] = value

    def __contains__(self, key: str) -> bool:
        return key in self.data

    def to_dict(self) -> dict[str, Any]:
        result = dict(self.data)
        if self.plotting_data:
            result['plotting_data'] = dict(self.plotting_data)
        return result
