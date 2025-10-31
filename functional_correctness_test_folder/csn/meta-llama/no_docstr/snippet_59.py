
from dataclasses import dataclass, field
from typing import Dict


@dataclass()
class _ErrorSummary:
    _executions: Dict[int, str] = field(default_factory=dict)
    _failed_count: int = field(default=0)

    def add_execution(self, index: int, name: str) -> None:
        self._executions[index] = name
        self._failed_count += 1

    @property
    def num_failed(self) -> int:
        return self._failed_count
