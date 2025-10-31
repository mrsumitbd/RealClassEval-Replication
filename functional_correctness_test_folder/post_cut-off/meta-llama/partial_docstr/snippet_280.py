
from typing import Optional


class BoundWorkerMethod:

    def __init__(self, wrapper: 'WorkerTaskWrapper', instance: object):
        self.wrapper = wrapper
        self.instance = instance
        self.pool = None

    def __call__(self, *args, **kwargs):
        return self.wrapper.func(self.instance, *args, **kwargs)

    def async_call(self, *args, **kwargs) -> str:
        return self.submit(*args, **kwargs)

    def submit(self, *args, **kwargs) -> str:
        if self.pool is None:
            return self.wrapper.default_pool.submit(self.wrapper.func, self.instance, *args, **kwargs)
        else:
            return self.pool.submit(self.wrapper.func, self.instance, *args, **kwargs)

    def run_and_wait(self, *args, timeout: Optional[float] = None, **kwargs):
        future = self.submit(*args, **kwargs)
        return future.result(timeout=timeout)

    def set_pool(self, pool: 'WorkerPool'):
        self.pool = pool

    def shutdown_default_pool(self):
        if self.pool is None:
            self.wrapper.default_pool.shutdown()

    def __getattr__(self, name):
        return getattr(self.wrapper, name)
