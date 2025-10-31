from typing import TYPE_CHECKING, Any, Callable, Optional

class HistoryManager:
    """
    Define a base context manager.

    It records a list of actions to be taken at a later time.
    This is used to implement context managers that allow temporary
    changes to a `cobra.core.Model`.

    """

    def __init__(self, **kwargs) -> None:
        """Initialize the class."""
        super().__init__(**kwargs)
        self._history = []

    def __call__(self, operation: Callable[[Any], Any]) -> None:
        """Add the corresponding operation to the history stack.

        Parameters
        ----------
        operation : callable
            A function to be called at a later time.

        """
        self._history.append(operation)

    def reset(self) -> None:
        """Trigger executions for all items in the stack in reverse order."""
        while self._history:
            entry = self._history.pop()
            entry()

    def size(self) -> int:
        """Calculate number of operations on the stack."""
        return len(self._history)