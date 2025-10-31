from typing import Optional


class BoundWorkerMethod:
    '''
    Proxy object that binds a `WorkerTaskWrapper` to an instance (self),
    allowing decorated instance methods to work seamlessly with all
    background execution capabilities.
    This enables you to use:
        instance.method()
        instance.method.async_call(...)
        instance.method.run_and_wait(...)
    without losing access to wrapper methods.
    Attributes:
        _wrapper: The original WorkerTaskWrapper
        _instance: The instance to bind as the first argument
    '''

    def __init__(self, wrapper: 'WorkerTaskWrapper', instance: object):
        '''
        Initialize the proxy with the wrapper and the instance.
        Args:
            wrapper: The WorkerTaskWrapper object
            instance: The object instance to bind to the call
        '''
        self._wrapper = wrapper
        self._instance = instance

    def __call__(self, *args, **kwargs):
        '''
        Synchronous execution with the bound instance.
        Equivalent to: wrapper(instance, *args, **kwargs)
        '''
        return self._wrapper(self._instance, *args, **kwargs)

    def async_call(self, *args, **kwargs) -> str:
        '''
        Asynchronous execution with the bound instance.
        Returns a worker_id.
        '''
        return self._wrapper.async_call(self._instance, *args, **kwargs)

    def submit(self, *args, **kwargs) -> str:
        '''
        Alias for async_call().
        '''
        return self.async_call(*args, **kwargs)

    def run_and_wait(self, *args, timeout: Optional[float] = None, **kwargs):
        '''
        Executes the task in the background, then waits for and returns the result.
        Raises:
            RuntimeError: if the task is cancelled
            Exception: if the task failed with an error
        '''
        return self._wrapper.run_and_wait(self._instance, *args, timeout=timeout, **kwargs)

    def set_pool(self, pool: 'WorkerPool'):
        '''
        Sets a specific pool to use for this task.
        '''
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
