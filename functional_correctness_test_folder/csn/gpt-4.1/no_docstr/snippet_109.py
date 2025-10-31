
from typing import Callable, Any


class HistoryManager:

    def __init__(self, **kwargs) -> None:
        self._history = []
        self._kwargs = kwargs

    def __call__(self, operation: Callable[[Any], Any]) -> None:
        self._history.append(operation)

    def reset(self) -> None:
        self._history.clear()

    def size(self) -> int:
        return len(self._history)
