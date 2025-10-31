
from dataclasses import dataclass, field
from typing import List, Tuple


@dataclass
class _ErrorSummary:
    _failures: List[Tuple[int, str]] = field(default_factory=list)

    def add_execution(self, index: int, name: str) -> None:
        """Record a failed execution with its index and name."""
        self._failures.append((index, name))

    @property
    def num_failed(self) -> int:
        """Return the number of recorded failed executions."""
        return len(self._failures)
