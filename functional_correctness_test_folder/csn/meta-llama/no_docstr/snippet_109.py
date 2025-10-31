
from typing import Callable, Any


class HistoryManager:

    def __init__(self, **kwargs) -> None:
        self.max_size = kwargs.get('max_size', float('inf'))
        self.history = []

    def __call__(self, operation: Callable[[Any], Any]) -> None:
        def wrapper(*args, **kwargs):
            result = operation(*args, **kwargs)
            self.history.append({
                'operation': operation.__name__,
                'args': args,
                'kwargs': kwargs,
                'result': result
            })
            if len(self.history) > self.max_size:
                self.history.pop(0)
            return result
        return wrapper

    def reset(self) -> None:
        self.history.clear()

    def size(self) -> int:
        return len(self.history)
