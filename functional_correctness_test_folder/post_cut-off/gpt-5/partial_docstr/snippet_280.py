from typing import Optional, Any


class BoundWorkerMethod:

    def __init__(self, wrapper: 'WorkerTaskWrapper', instance: object):
        self._wrapper = wrapper
        self._instance = instance
        self._bound_pool: Optional['WorkerPool'] = None

    def __call__(self, *args, **kwargs):
        if hasattr(self._wrapper, 'run_and_wait'):
            return self._wrapper.run_and_wait(self._instance, *args, **kwargs)
        if callable(self._wrapper):
            return self._wrapper(self._instance, *args, **kwargs)
        raise AttributeError(
            "Underlying wrapper is not callable and has no 'run_and_wait'.")

    def async_call(self, *args, **kwargs) -> str:
        if hasattr(self._wrapper, 'async_call'):
            return self._wrapper.async_call(self._instance, *args, **kwargs)
        if hasattr(self._wrapper, 'submit'):
            return self._wrapper.submit(self._instance, *args, **kwargs)
        raise AttributeError(
            "Underlying wrapper has neither 'async_call' nor 'submit'.")

    def submit(self, *args, **kwargs) -> str:
        if hasattr(self._wrapper, 'submit'):
            return self._wrapper.submit(self._instance, *args, **kwargs)
        if hasattr(self._wrapper, 'async_call'):
            return self._wrapper.async_call(self._instance, *args, **kwargs)
        raise AttributeError(
            "Underlying wrapper has neither 'submit' nor 'async_call'.")

    def run_and_wait(self, *args, timeout: Optional[float] = None, **kwargs):
        if hasattr(self._wrapper, 'run_and_wait'):
            return self._wrapper.run_and_wait(self._instance, *args, timeout=timeout, **kwargs)
        if callable(self._wrapper):
            return self._wrapper(self._instance, *args, **kwargs)
        raise AttributeError(
            "Underlying wrapper has no 'run_and_wait' and is not callable.")

    def set_pool(self, pool: 'WorkerPool'):
        '''
        Sets a specific pool to use for this task.
        '''
        self._bound_pool = pool
        if hasattr(self._wrapper, 'set_pool'):
            self._wrapper.set_pool(pool)

    def shutdown_default_pool(self):
        '''
        Shuts down the default pool used by this function, if created.
        '''
        if hasattr(self._wrapper, 'shutdown_default_pool'):
            return self._wrapper.shutdown_default_pool()
        return None

    def __getattr__(self, name):
        '''
        Fallback to the wrapper’s attributes for completeness.
        This makes sure any missing attributes are forwarded.
        '''
        return getattr(self._wrapper, name)
