from dataclasses import dataclass, field
from typing import List, Tuple


@dataclass()
class _ErrorSummary:
    executions: List[Tuple[int, str]] = field(default_factory=list)

    def add_execution(self, index: int, name: str) -> None:
        if not isinstance(index, int):
            raise TypeError("index must be an int")
        if not isinstance(name, str):
            raise TypeError("name must be a str")
        self.executions.append((index, name))

    @property
    def num_failed(self) -> int:
        return len(self.executions)
