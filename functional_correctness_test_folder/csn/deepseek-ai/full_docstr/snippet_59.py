
from dataclasses import dataclass
from typing import Dict, List


@dataclass
class _ErrorSummary:
    '''Contains data for errors of a node.'''
    _executions: Dict[int, str] = None

    def __post_init__(self):
        if self._executions is None:
            self._executions = {}

    def add_execution(self, index: int, name: str) -> None:
        '''Adds an execution to the summary.'''
        self._executions[index] = name

    @property
    def num_failed(self) -> int:
        '''Helps with jinja'''
        return len(self._executions)
