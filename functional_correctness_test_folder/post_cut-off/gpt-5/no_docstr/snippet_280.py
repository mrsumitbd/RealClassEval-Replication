from typing import Optional, Any


class BoundWorkerMethod:

    def __init__(self, wrapper: 'WorkerTaskWrapper', instance: object):
        self._wrapper = wrapper
        self._instance = instance

    def __call__(self, *args, **kwargs):
        return self.run_and_wait(*args, **kwargs)

    def async_call(self, *args, **kwargs) -> str:
        submit = getattr(self._wrapper, "submit", None)
        if submit is None:
            raise AttributeError(
                "Underlying wrapper does not support submit/async_call")
        return submit(self._instance, *args, **kwargs)

    def submit(self, *args, **kwargs) -> str:
        submit = getattr(self._wrapper, "submit", None)
        if submit is None:
            raise AttributeError("Underlying wrapper does not support submit")
        return submit(self._instance, *args, **kwargs)

    def run_and_wait(self, *args, timeout: Optional[float] = None, **kwargs):
        run_and_wait = getattr(self._wrapper, "run_and_wait", None)
        if run_and_wait is None:
            raise AttributeError(
                "Underlying wrapper does not support run_and_wait")
        return run_and_wait(self._instance, *args, timeout=timeout, **kwargs)

    def set_pool(self, pool: 'WorkerPool'):
        set_pool = getattr(self._wrapper, "set_pool", None)
        if set_pool is None:
            raise AttributeError(
                "Underlying wrapper does not support set_pool")
        set_pool(pool)

    def shutdown_default_pool(self):
        shutdown = getattr(self._wrapper, "shutdown_default_pool", None)
        if shutdown is None:
            raise AttributeError(
                "Underlying wrapper does not support shutdown_default_pool")
        shutdown()

    def __getattr__(self, name):
        try:
            return getattr(self._wrapper, name)
        except AttributeError:
            raise AttributeError(
                f"{self.__class__.__name__} has no attribute '{name}'") from None
