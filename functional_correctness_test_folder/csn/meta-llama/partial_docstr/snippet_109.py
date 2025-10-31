
from typing import Callable, Any


class HistoryManager:

    def __init__(self, **kwargs) -> None:
        '''Initialize the class.'''
        self._history = []
        self._kwargs = kwargs

    def __call__(self, operation: Callable[[Any], Any]) -> Callable[[Any], Any]:
        '''Wrap the given operation and store it in the history.'''
        def wrapper(*args, **kwargs):
            result = operation(*args, **kwargs)
            self._history.append((operation, args, kwargs, result))
            return result
        return wrapper

    def reset(self) -> None:
        '''Trigger executions for all items in the stack in reverse order.'''
        for operation, args, kwargs, _ in reversed(self._history):
            operation(*args, **kwargs)

    def size(self) -> int:
        '''Calculate number of operations on the stack.'''
        return len(self._history)
