from typing import Any, Callable, Optional
from concurrent.futures import Future, TimeoutError

class Task:

    def __init__(self, identifier: int, future: Future, timeout: Optional[float], payload: 'TaskPayload'):
        self.id = identifier
        self.future = future
        self.timeout = timeout
        self.payload = payload
        self.timestamp = 0.0
        self.worker_id = 0

    @property
    def started(self) -> bool:
        return bool(self.timestamp > 0)

    def set_running_or_notify_cancel(self):
        if hasattr(self.future, 'map_future'):
            if not self.future.map_future.done():
                try:
                    self.future.map_future.set_running_or_notify_cancel()
                except RuntimeError:
                    pass
        try:
            self.future.set_running_or_notify_cancel()
        except RuntimeError:
            pass