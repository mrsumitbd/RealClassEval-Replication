from typing import Any, Callable, List


class HistoryManager:
    '''
    Define a base context manager.
    It records a list of actions to be taken at a later time.
    This is used to implement context managers that allow temporary
    changes to a `cobra.core.Model`.
    '''

    def __init__(self, **kwargs) -> None:
        '''Initialize the class.'''
        self._history: List[Callable[[], Any]] = []

    def __call__(self, operation: Callable[[Any], Any]) -> None:
        '''Add the corresponding operation to the history stack.
        Parameters
        ----------
        operation : callable
            A function to be called at a later time.
        '''
        if not callable(operation):
            raise TypeError("operation must be callable")
        # Store as-is; operations are expected to be closures needing no args
        self._history.append(operation)

    def reset(self) -> None:
        '''Trigger executions for all items in the stack in reverse order.'''
        errors = []
        try:
            for op in reversed(self._history):
                try:
                    op()
                except Exception as exc:
                    errors.append(exc)
        finally:
            self._history.clear()
        if errors:
            if len(errors) == 1:
                raise errors[0]
            raise RuntimeError(
                f"{len(errors)} errors occurred during reset") from errors[0]

    def size(self) -> int:
        '''Calculate number of operations on the stack.'''
        return len(self._history)
