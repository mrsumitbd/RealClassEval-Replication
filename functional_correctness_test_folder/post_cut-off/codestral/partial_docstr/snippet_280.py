
class BoundWorkerMethod:

    def __init__(self, wrapper: 'WorkerTaskWrapper', instance: object):

        self.wrapper = wrapper
        self.instance = instance
        self.pool = None

    def __call__(self, *args, **kwargs):

        return self.wrapper(self.instance, *args, **kwargs)

    def async_call(self, *args, **kwargs) -> str:

        return self.wrapper.async_call(self.instance, *args, **kwargs)

    def submit(self, *args, **kwargs) -> str:

        return self.wrapper.submit(self.instance, *args, **kwargs)

    def run_and_wait(self, *args, timeout: Optional[float] = None, **kwargs):

        return self.wrapper.run_and_wait(self.instance, *args, timeout=timeout, **kwargs)

    def set_pool(self, pool: 'WorkerPool'):

        self.pool = pool

    def shutdown_default_pool(self):

        if self.pool is not None:
            self.pool.shutdown()

    def __getattr__(self, name):

        return getattr(self.wrapper, name)
