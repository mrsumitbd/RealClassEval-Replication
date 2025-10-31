
from dataclasses import dataclass, field


@dataclass()
class _ErrorSummary:
    _executions: list = field(default_factory=list)

    def add_execution(self, index: int, name: str) -> None:
        self._executions.append((index, name))

    @property
    def num_failed(self) -> int:
        return len(self._executions)
