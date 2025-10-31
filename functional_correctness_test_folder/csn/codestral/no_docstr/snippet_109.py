
from typing import Any, Callable


class HistoryManager:

    def __init__(self, **kwargs) -> None:
        self.history = []
        self.current_index = -1

    def __call__(self, operation: Callable[[Any], Any]) -> None:
        if self.current_index < len(self.history) - 1:
            self.history = self.history[:self.current_index + 1]
        result = operation()
        self.history.append(result)
        self.current_index += 1

    def reset(self) -> None:
        self.history = []
        self.current_index = -1

    def size(self) -> int:
        return len(self.history)
