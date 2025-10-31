from typing import Callable, Generator, List
import time

class Task:

    def __init__(self, g: Generator, delay: float, next_run: float=None, name: str=None) -> None:
        self.g = g
        g.send(None)
        self.delay = delay
        self.next_run = next_run if next_run else time.time()
        self.name = name if name is not None else self.g.__name__

    def __str__(self) -> str:
        return f'<{self.name} (delay={self.delay})>'

    def __next__(self) -> None:
        return next(self.g)

    def send(self, obj) -> None:
        return self.g.send(obj)
    __repr__ = __str__