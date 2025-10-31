from typing import Any, Callable, List


class HistoryManager:

    def __init__(self, **kwargs) -> None:
        '''Initialize the class.'''
        self._stack: List[Callable[[Any], Any]] = []
        self._context: Any = kwargs.get("context", None)
        self._raise_on_error: bool = bool(kwargs.get("raise_on_error", False))

    def __call__(self, operation: Callable[[Any], Any]) -> None:
        if not callable(operation):
            raise TypeError("operation must be callable")
        self._stack.append(operation)

    def reset(self) -> None:
        '''Trigger executions for all items in the stack in reverse order.'''
        while self._stack:
            op = self._stack.pop()
            try:
                op(self._context)
            except Exception:
                if self._raise_on_error:
                    raise

    def size(self) -> int:
        '''Calculate number of operations on the stack.'''
        return len(self._stack)
