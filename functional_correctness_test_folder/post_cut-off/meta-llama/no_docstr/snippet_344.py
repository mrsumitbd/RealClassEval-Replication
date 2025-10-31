
from dataclasses import dataclass, asdict
from typing import Any


@dataclass
class OptimizationResults:
    """Class to store optimization results."""

    def __post_init__(self):
        self._data = {}

    def update_plotting_data(self, **kwargs):
        self._data.update(kwargs)

    def get(self, key: str, default: Any = None) -> Any:
        return self._data.get(key, default)

    def __getitem__(self, key: str) -> Any:
        return self._data[key]

    def __setitem__(self, key: str, value: Any):
        self._data[key] = value

    def __contains__(self, key: str) -> bool:
        return key in self._data

    def to_dict(self) -> dict[str, Any]:
        result = asdict(self)
        result.update(self._data)
        return result
