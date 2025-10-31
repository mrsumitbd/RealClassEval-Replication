
from typing import Optional


class BoundWorkerMethod:

    def __init__(self, wrapper: 'WorkerTaskWrapper', instance: object):
        self.wrapper = wrapper
        self.instance = instance
        self.pool = None

    def __call__(self, *args, **kwargs):
        return self.wrapper.func(self.instance, *args, **kwargs)

    def async_call(self, *args, **kwargs) -> str:
        task = self.wrapper.create_task(self.instance, *args, **kwargs)
        if self.pool is not None:
            return self.pool.submit_task(task)
        else:
            return task.submit()

    def submit(self, *args, **kwargs) -> str:
        return self.async_call(*args, **kwargs)

    def run_and_wait(self, *args, timeout: Optional[float] = None, **kwargs):
        task_id = self.async_call(*args, **kwargs)
        return self.wrapper.wait_task(task_id, timeout)

    def set_pool(self, pool: 'WorkerPool'):
        self.pool = pool

    def shutdown_default_pool(self):
        if self.pool is not None:
            self.pool.shutdown()

    def __getattr__(self, name):
        return getattr(self.wrapper.func, name)
