
from typing import Any, Callable


class HistoryManager:

    def __init__(self, **kwargs) -> None:
        '''Initialize the class.'''
        self.stack = []
        self.kwargs = kwargs

    def __call__(self, operation: Callable[[Any], Any]) -> None:
        self.stack.append(operation)

    def reset(self) -> None:
        '''Trigger executions for all items in the stack in reverse order.'''
        for operation in reversed(self.stack):
            operation(**self.kwargs)
        self.stack.clear()

    def size(self) -> int:
        '''Calculate number of operations on the stack.'''
        return len(self.stack)
