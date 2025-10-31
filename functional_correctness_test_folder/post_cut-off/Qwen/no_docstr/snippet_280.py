
from typing import Optional, Any, Callable
import threading
import queue


class WorkerTaskWrapper:
    def __init__(self, func: Callable):
        self.func = func

    def __call__(self, *args, **kwargs) -> Any:
        return self.func(*args, **kwargs)


class WorkerPool:
    def __init__(self, num_workers: int):
        self.tasks = queue.Queue()
        self.workers = [threading.Thread(target=self.worker)
                        for _ in range(num_workers)]
        for worker in self.workers:
            worker.start()

    def worker(self):
        while True:
            func, args, kwargs = self.tasks.get()
            if func is None:
                break
            func(*args, **kwargs)
            self.tasks.task_done()

    def submit(self, func: Callable, *args, **kwargs) -> None:
        self.tasks.put((func, args, kwargs))

    def shutdown(self, wait: bool = True) -> None:
        for _ in self.workers:
            self.tasks.put((None, (), {}))
        for worker in self.workers:
            worker.join() if wait else None


class BoundWorkerMethod:
    _default_pool = WorkerPool(4)

    def __init__(self, wrapper: 'WorkerTaskWrapper', instance: object):
        self.wrapper = wrapper
        self.instance = instance
        self.pool = self._default_pool

    def __call__(self, *args, **kwargs):
        return self.wrapper(self.instance, *args, **kwargs)

    def async_call(self, *args, **kwargs) -> str:
        result = []

        def target():
            result.append(self.wrapper(self.instance, *args, **kwargs))
        self.pool.submit(target)
        return "Task submitted"

    def submit(self, *args, **kwargs) -> str:
        self.pool.submit(self.wrapper, self.instance, *args, **kwargs)
        return "Task submitted"

    def run_and_wait(self, *args, timeout: Optional[float] = None, **kwargs):
        result = []

        def target():
            result.append(self.wrapper(self.instance, *args, **kwargs))
        self.pool.submit(target)
        self.pool.tasks.join(timeout=timeout)
        return result[0] if result else None

    def set_pool(self, pool: 'WorkerPool'):
        self.pool = pool

    def shutdown_default_pool(self):
        self._default_pool.shutdown()

    def __getattr__(self, name):
        return getattr(self.instance, name)
