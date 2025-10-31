
from dataclasses import dataclass
from typing import Dict, List


@dataclass
class _ErrorSummary:
    _executions: Dict[int, str] = None

    def __post_init__(self):
        if self._executions is None:
            self._executions = {}

    def add_execution(self, index: int, name: str) -> None:
        self._executions[index] = name

    @property
    def num_failed(self) -> int:
        return len(self._executions)
