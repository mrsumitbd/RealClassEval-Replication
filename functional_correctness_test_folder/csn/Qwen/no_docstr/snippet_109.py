
from typing import Callable, Any, List


class HistoryManager:

    def __init__(self, **kwargs) -> None:
        self.history: List[Callable[[Any], Any]] = []

    def __call__(self, operation: Callable[[Any], Any]) -> None:
        self.history.append(operation)

    def reset(self) -> None:
        self.history.clear()

    def size(self) -> int:
        return len(self.history)
