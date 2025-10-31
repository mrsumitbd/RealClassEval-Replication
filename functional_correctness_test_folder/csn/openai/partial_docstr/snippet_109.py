
from typing import Any, Callable, List


class HistoryManager:
    def __init__(self, **kwargs) -> None:
        """Initialize the class."""
        # Store the history stack
        self._stack: List[Callable[[Any], Any]] = []

    def __call__(self, operation: Callable[[Any], Any]) -> None:
        """Add an operation to the history stack."""
        self._stack.append(operation)

    def reset(self) -> None:
        """Trigger executions for all items in the stack in reverse order."""
        # Execute each operation in reverse order
        for op in reversed(self._stack):
            try:
                # Try calling without arguments first
                op()
            except TypeError:
                # If the operation expects an argument, call with None
                op(None)
        # Clear the stack after execution
        self._stack.clear()

    def size(self) -> int:
        """Calculate number of operations on the stack."""
        return len(self._stack)
