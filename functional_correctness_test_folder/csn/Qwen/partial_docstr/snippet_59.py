
from dataclasses import dataclass, field
from typing import List, Tuple


@dataclass()
class _ErrorSummary:
    '''Contains data for errors of a node.'''
    _executions: List[Tuple[int, str]] = field(default_factory=list)
    _failed_count: int = 0

    def add_execution(self, index: int, name: str) -> None:
        '''Adds an execution to the summary.'''
        self._executions.append((index, name))
        # Assuming an execution is failed if its name contains 'error'
        if 'error' in name.lower():
            self._failed_count += 1

    @property
    def num_failed(self) -> int:
        return self._failed_count
