
class BoundWorkerMethod:

    def __init__(self, wrapper: 'WorkerTaskWrapper', instance: object):
        self._wrapper = wrapper
        self._instance = instance
        self._pool = None

    def __call__(self, *args, **kwargs):
        return self.run_and_wait(*args, **kwargs)

    def async_call(self, *args, **kwargs) -> str:
        return self._wrapper.async_call(self._instance, *args, **kwargs)

    def submit(self, *args, **kwargs) -> str:
        return self._wrapper.submit(self._instance, *args, **kwargs)

    def run_and_wait(self, *args, timeout: Optional[float] = None, **kwargs):
        return self._wrapper.run_and_wait(self._instance, *args, timeout=timeout, **kwargs)

    def set_pool(self, pool: 'WorkerPool'):
        '''
        Sets a specific pool to use for this task.
        '''
        self._pool = pool
        self._wrapper.set_pool(pool)

    def shutdown_default_pool(self):
        '''
        Shuts down the default pool used by this function, if created.
        '''
        self._wrapper.shutdown_default_pool()

    def __getattr__(self, name):
        '''
        Fallback to the wrapper’s attributes for completeness.
        This makes sure any missing attributes are forwarded.
        '''
        return getattr(self._wrapper, name)
