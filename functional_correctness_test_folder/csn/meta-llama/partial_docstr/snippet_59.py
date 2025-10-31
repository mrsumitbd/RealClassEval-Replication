
from dataclasses import dataclass, field
from typing import Dict, Set


@dataclass()
class _ErrorSummary:
    '''Contains data for errors of a node.'''
    executions: Dict[str, Set[int]] = field(default_factory=dict)

    def add_execution(self, index: int, name: str) -> None:
        '''Adds an execution to the summary.'''
        if name not in self.executions:
            self.executions[name] = set()
        self.executions[name].add(index)

    @property
    def num_failed(self) -> int:
        '''Returns the total number of failed executions.'''
        return sum(len(indices) for indices in self.executions.values())
