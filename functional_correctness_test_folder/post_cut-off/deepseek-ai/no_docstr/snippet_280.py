
class BoundWorkerMethod:

    def __init__(self, wrapper: 'WorkerTaskWrapper', instance: object):
        self._wrapper = wrapper
        self._instance = instance
        self._pool = None

    def __call__(self, *args, **kwargs):
        return self.run_and_wait(*args, **kwargs)

    def async_call(self, *args, **kwargs) -> str:
        return self.submit(*args, **kwargs)

    def submit(self, *args, **kwargs) -> str:
        if self._pool is None:
            raise RuntimeError("No worker pool set")
        return self._pool.submit(self._wrapper, self._instance, *args, **kwargs)

    def run_and_wait(self, *args, timeout: Optional[float] = None, **kwargs):
        task_id = self.submit(*args, **kwargs)
        return self._pool.wait_for_task(task_id, timeout=timeout)

    def set_pool(self, pool: 'WorkerPool'):
        self._pool = pool

    def shutdown_default_pool(self):
        if self._pool is not None:
            self._pool.shutdown()

    def __getattr__(self, name):
        return getattr(self._wrapper, name)
