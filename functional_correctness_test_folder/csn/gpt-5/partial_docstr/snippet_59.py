from dataclasses import dataclass, field
from typing import List, Tuple


@dataclass()
class _ErrorSummary:
    '''Contains data for errors of a node.'''
    executions: List[Tuple[int, str]] = field(default_factory=list)

    def add_execution(self, index: int, name: str) -> None:
        '''Adds an execution to the summary.'''
        self.executions.append((index, name))

    @property
    def num_failed(self) -> int:
        return len(self.executions)
