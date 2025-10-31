
from typing import Callable, Any


class HistoryManager:

    def __init__(self, **kwargs) -> None:
        '''Initialize the class.'''
        self.stack = []
        for key, value in kwargs.items():
            self.stack.append((key, value))

    def __call__(self, operation: Callable[[Any], Any]) -> None:
        for i, (key, value) in enumerate(self.stack):
            self.stack[i] = (key, operation(value))

    def reset(self) -> None:
        '''Trigger executions for all items in the stack in reverse order.'''
        for key, value in reversed(self.stack):
            if callable(value):
                value()

    def size(self) -> int:
        '''Calculate number of operations on the stack.'''
        return len(self.stack)
