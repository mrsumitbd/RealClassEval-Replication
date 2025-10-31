
from typing import Optional


class BoundWorkerMethod:

    def __init__(self, wrapper: 'WorkerTaskWrapper', instance: object):
        self._wrapper = wrapper
        self._instance = instance
        self._pool = None

    def __call__(self, *args, **kwargs):
        return self._wrapper(self._instance, *args, **kwargs)

    def async_call(self, *args, **kwargs) -> str:
        pool = self._pool if self._pool is not None else self._wrapper.get_default_pool()
        return pool.submit(self._wrapper, self._instance, *args, **kwargs)

    def submit(self, *args, **kwargs) -> str:
        return self.async_call(*args, **kwargs)

    def run_and_wait(self, *args, timeout: Optional[float] = None, **kwargs):
        pool = self._pool if self._pool is not None else self._wrapper.get_default_pool()
        job_id = pool.submit(self._wrapper, self._instance, *args, **kwargs)
        return pool.get_result(job_id, timeout=timeout)

    def set_pool(self, pool: 'WorkerPool'):
        '''
        Sets a specific pool to use for this task.
        '''
        self._pool = pool

    def shutdown_default_pool(self):
        '''
        Shuts down the default pool used by this function, if created.
        '''
        pool = self._wrapper.get_default_pool(create=False)
        if pool is not None:
            pool.shutdown()

    def __getattr__(self, name):
        '''
        Fallback to the wrapper’s attributes for completeness.
        This makes sure any missing attributes are forwarded.
        '''
        return getattr(self._wrapper, name)
