
from __future__ import annotations

from typing import Any, Callable, List, Optional


class HistoryManager:
    """
    Define a base context manager.
    It records a list of actions to be taken at a later time.
    This is used to implement context managers that allow temporary
    changes to a `cobra.core.Model`.
    """

    def __init__(self, **kwargs: Any) -> None:
        """Initialize the class."""
        self._stack: List[Callable[[], Any]] = []
        self._kwargs = kwargs

    def __call__(self, operation: Callable[[Any], Any]) -> None:
        """
        Add the corresponding operation to the history stack.
        Parameters
        ----------
        operation : callable
            A function to be called at a later time.
        """
        self._stack.append(operation)

    def reset(self) -> None:
        """Trigger executions for all items in the stack in reverse order."""
        for op in reversed(self._stack):
            op()
        self._stack.clear()

    def size(self) -> int:
        """Calculate number of operations on the stack."""
        return len(self._stack)

    # Optional context manager support
    def __enter__(self) -> "HistoryManager":
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> Optional[bool]:
        self.reset()
        return None
