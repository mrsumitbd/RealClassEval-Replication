
from dataclasses import dataclass, field


@dataclass()
class _ErrorSummary:
    '''Contains data for errors of a node.'''
    _executions: list = field(default_factory=list, init=False, repr=False)

    def add_execution(self, index: int, name: str) -> None:
        '''Adds an execution to the summary.'''
        self._executions.append((index, name))

    @property
    def num_failed(self) -> int:
        '''Helps with jinja'''
        return len(self._executions)
