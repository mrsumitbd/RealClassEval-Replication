from threading import RLock
import itertools
from typing import Any, Callable, Optional
from queue import Queue

class PoolContext:

    def __init__(self, max_workers: int, max_tasks: int, initializer: Callable, initargs: list):
        self._status = PoolStatus.CREATED
        self.status_mutex = RLock()
        self.task_queue = Queue()
        self.workers = max_workers
        self.task_counter = itertools.count()
        self.worker_parameters = Worker(max_tasks, initializer, initargs)

    @property
    def status(self) -> int:
        return self._status

    @status.setter
    def status(self, status: int):
        with self.status_mutex:
            if self.alive:
                self._status = status

    @property
    def alive(self) -> bool:
        return self.status not in (PoolStatus.ERROR, PoolStatus.STOPPED)