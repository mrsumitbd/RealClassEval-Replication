
from typing import Optional, Any


class BoundWorkerMethod:
    """
    A bound method that delegates calls to a WorkerTaskWrapper.
    """

    def __init__(self, wrapper: 'WorkerTaskWrapper', instance: object):
        """
        Store the wrapper and the instance to which the method is bound.
        """
        self.wrapper = wrapper
        self.instance = instance
        self.pool: Optional['WorkerPool'] = None

    def __call__(self, *args, **kwargs):
        """
        Synchronously invoke the wrapped method on the bound instance.
        """
        return self.wrapper(self.instance, *args, **kwargs)

    def async_call(self, *args, **kwargs) -> str:
        """
        Asynchronously invoke the wrapped method on the bound instance.
        Returns a task identifier.
        """
        if hasattr(self.wrapper, "async_call"):
            return self.wrapper.async_call(self.instance, *args, **kwargs)
        # Fallback: submit to a pool if available
        if self.pool is not None:
            return self.pool.submit(self.wrapper, self.instance, *args, **kwargs)
        # If no async support, raise an error
        raise RuntimeError(
            "The wrapper does not support async_call and no pool is set.")

    def submit(self, *args, **kwargs) -> str:
        """
        Submit the wrapped method to a worker pool.
        Returns a task identifier.
        """
        if self.pool is not None:
            return self.pool.submit(self.wrapper, self.instance, *args, **kwargs)
        # If no pool is set, fall back to async_call
        return self.async_call(*args, **kwargs)

    def run_and_wait(self, *args, timeout: Optional[float] = None, **kwargs):
        """
        Run the wrapped method asynchronously and wait for the result.
        """
        try:
            task_id = self.async_call(*args, **kwargs)
            if hasattr(self.wrapper, "wait"):
                return self.wrapper.wait(task_id, timeout=timeout)
            # If wrapper has no wait, try pool's wait
            if self.pool is not None and hasattr(self.pool, "wait"):
                return self.pool.wait(task_id, timeout=timeout)
            # Fallback to synchronous call
            return self.wrapper(self.instance, *args, **kwargs)
        except Exception:
            # If async path fails, fall back to synchronous call
            return self.wrapper(self.instance, *args, **kwargs)

    def set_pool(self, pool: 'WorkerPool'):
        """
        Sets a specific pool to use for this task.
        """
        self.pool = pool

    def shutdown_default_pool(self):
        """
        Shuts down the default pool used by this function, if created.
        """
        if self.pool is not None and hasattr(self.pool, "shutdown"):
            self.pool.shutdown()

    def __getattr__(self, name):
        """
        Fallback to the wrapper’s attributes for completeness.
        This makes sure any missing attributes are forwarded.
        """
        return getattr(self.wrapper, name)
