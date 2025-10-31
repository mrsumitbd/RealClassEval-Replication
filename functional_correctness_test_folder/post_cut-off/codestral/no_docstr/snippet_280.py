
class BoundWorkerMethod:

    def __init__(self, wrapper: 'WorkerTaskWrapper', instance: object):

        self.wrapper = wrapper
        self.instance = instance
        self.pool = None

    def __call__(self, *args, **kwargs):

        return self.wrapper(self.instance, *args, **kwargs)

    def async_call(self, *args, **kwargs) -> str:

        if self.pool is None:
            raise RuntimeError("No pool set for async_call")
        return self.pool.submit(self.wrapper, self.instance, *args, **kwargs)

    def submit(self, *args, **kwargs) -> str:

        return self.async_call(*args, **kwargs)

    def run_and_wait(self, *args, timeout: Optional[float] = None, **kwargs):

        if self.pool is None:
            raise RuntimeError("No pool set for run_and_wait")
        future = self.pool.submit(self.wrapper, self.instance, *args, **kwargs)
        return self.pool.wait(future, timeout)

    def set_pool(self, pool: 'WorkerPool'):

        self.pool = pool

    def shutdown_default_pool(self):

        if self.pool is not None:
            self.pool.shutdown()
            self.pool = None

    def __getattr__(self, name):

        if name in self.wrapper.__dict__:
            return getattr(self.wrapper, name)
        raise AttributeError(
            f"'{self.__class__.__name__}' object has no attribute '{name}'")
