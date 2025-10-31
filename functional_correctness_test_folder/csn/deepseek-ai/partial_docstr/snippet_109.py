
from typing import Any, Callable, List


class HistoryManager:

    def __init__(self, **kwargs) -> None:
        '''Initialize the class.'''
        self._stack: List[Callable[[Any], Any]] = []

    def __call__(self, operation: Callable[[Any], Any]) -> None:
        self._stack.append(operation)

    def reset(self) -> None:
        '''Trigger executions for all items in the stack in reverse order.'''
        for operation in reversed(self._stack):
            operation()
        self._stack.clear()

    def size(self) -> int:
        '''Calculate number of operations on the stack.'''
        return len(self._stack)
