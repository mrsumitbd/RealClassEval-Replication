
from typing import Any, Callable, List


class HistoryManager:

    def __init__(self, **kwargs) -> None:
        self._history: List[Any] = []

    def __call__(self, operation: Callable[[Any], Any]) -> None:
        result = operation(self._history.copy())
        self._history.append(result)

    def reset(self) -> None:
        self._history.clear()

    def size(self) -> int:
        return len(self._history)
