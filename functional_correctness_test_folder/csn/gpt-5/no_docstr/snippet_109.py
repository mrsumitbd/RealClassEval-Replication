from typing import Any, Callable, List


class HistoryManager:
    def __init__(self, **kwargs) -> None:
        self._history: List[Callable[[Any], Any]] = []
        self._capacity: int | None = kwargs.get("capacity")

    def __call__(self, operation: Callable[[Any], Any]) -> None:
        if not callable(operation):
            raise TypeError("operation must be callable")
        if self._capacity is not None and self._capacity <= 0:
            return
        if self._capacity is not None and len(self._history) >= self._capacity:
            # Maintain a fixed-size history by dropping the oldest entry
            self._history.pop(0)
        self._history.append(operation)

    def reset(self) -> None:
        self._history.clear()

    def size(self) -> int:
        return len(self._history)
