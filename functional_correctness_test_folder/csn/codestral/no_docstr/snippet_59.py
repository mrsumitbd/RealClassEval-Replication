
from dataclasses import dataclass, field


@dataclass()
class _ErrorSummary:
    executions: list = field(default_factory=list)

    def add_execution(self, index: int, name: str) -> None:
        self.executions.append((index, name))

    @property
    def num_failed(self) -> int:
        return len(self.executions)
