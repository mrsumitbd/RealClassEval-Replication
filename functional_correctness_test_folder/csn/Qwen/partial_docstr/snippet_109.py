
from typing import Callable, Any, List


class HistoryManager:

    def __init__(self, **kwargs) -> None:
        '''Initialize the class.'''
        self._history: List[Callable[[Any], Any]] = []

    def __call__(self, operation: Callable[[Any], Any]) -> None:
        self._history.append(operation)

    def reset(self) -> None:
        '''Trigger executions for all items in the stack in reverse order.'''
        while self._history:
            operation = self._history.pop()
            operation()

    def size(self) -> int:
        '''Calculate number of operations on the stack.'''
        return len(self._history)
