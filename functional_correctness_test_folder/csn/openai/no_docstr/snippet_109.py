
from typing import Any, Callable, List, Tuple


class HistoryManager:
    """
    A simple history manager that records the operations executed via the
    instance callable interface. Each operation is stored along with its
    result. The manager can be reset and its size queried.
    """

    def __init__(self, max_size: int | None = None, **kwargs) -> None:
        """
        Parameters
        ----------
        max_size : int | None, optional
            Maximum number of history entries to keep. If None, history
            grows indefinitely.
        **kwargs
            Any additional attributes to set on the instance.
        """
        self.max_size: int | None = max_size
        self._history: List[Tuple[Callable[[Any], Any], Any]] = []

        # Set any extra keyword arguments as attributes
        for key, value in kwargs.items():
            setattr(self, key, value)

    def __call__(self, operation: Callable[[Any], Any]) -> None:
        """
        Execute the given operation and record it in the history.

        Parameters
        ----------
        operation : Callable[[Any], Any]
            A callable that takes no arguments and returns a value.
        """
        # Execute the operation
        result = operation()

        # Store the operation and its result
        self._history.append((operation, result))

        # Enforce maximum history size if specified
        if self.max_size is not None and len(self._history) > self.max_size:
            # Remove the oldest entry
            self._history.pop(0)

    def reset(self) -> None:
        """
        Clear the history.
        """
        self._history.clear()

    def size(self) -> int:
        """
        Return the number of recorded operations.

        Returns
        -------
        int
            The size of the history.
        """
        return len(self._history)
