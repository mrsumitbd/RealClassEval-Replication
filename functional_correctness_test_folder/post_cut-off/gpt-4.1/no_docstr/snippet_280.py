
from typing import Optional


class BoundWorkerMethod:
    def __init__(self, wrapper: 'WorkerTaskWrapper', instance: object):
        self._wrapper = wrapper
        self._instance = instance
        self._pool = None

    def __call__(self, *args, **kwargs):
        return self.run_and_wait(*args, **kwargs)

    def async_call(self, *args, **kwargs) -> str:
        pool = self._pool or self._wrapper.default_pool
        return pool.submit(self._wrapper, self._instance, args, kwargs)

    def submit(self, *args, **kwargs) -> str:
        return self.async_call(*args, **kwargs)

    def run_and_wait(self, *args, timeout: Optional[float] = None, **kwargs):
        pool = self._pool or self._wrapper.default_pool
        task_id = pool.submit(self._wrapper, self._instance, args, kwargs)
        return pool.get_result(task_id, timeout=timeout)

    def set_pool(self, pool: 'WorkerPool'):
        self._pool = pool

    def shutdown_default_pool(self):
        if hasattr(self._wrapper, 'default_pool') and self._wrapper.default_pool:
            self._wrapper.default_pool.shutdown()

    def __getattr__(self, name):
        return getattr(self._wrapper, name)
