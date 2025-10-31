from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Mapping


@dataclass
class OptimizationResults:
    data: dict[str, Any] = field(default_factory=dict)
    plotting: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self):
        if not isinstance(self.data, Mapping):
            raise TypeError("data must be a mapping")
        if not isinstance(self.plotting, Mapping):
            raise TypeError("plotting must be a mapping")
        self.data = dict(self.data)
        self.plotting = dict(self.plotting)

    def update_plotting_data(self, **kwargs):
        self.plotting.update(kwargs)

    def get(self, key: str, default: Any = None) -> Any:
        return self.data.get(key, default)

    def __getitem__(self, key: str) -> Any:
        return self.data[key]

    def __setitem__(self, key: str, value: Any):
        self.data[key] = value

    def __contains__(self, key: str) -> bool:
        return key in self.data

    def update_plotting_data(self, **kwargs):
        self.plotting.update(kwargs)

    def to_dict(self) -> dict[str, Any]:
        return {
            "data": dict(self.data),
            "plotting": dict(self.plotting),
        }
