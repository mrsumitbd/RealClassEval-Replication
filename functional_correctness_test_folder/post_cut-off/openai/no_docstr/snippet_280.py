
from __future__ import annotations
from typing import Optional, Any, Tuple, Dict


class BoundWorkerMethod:
    """
    A descriptor that binds a method to a worker pool.  The wrapper is
    expected to provide a ``run`` method that accepts the instance and
    the method arguments.  The pool is expected to provide ``submit``,
    ``get_result`` and ``shutdown`` methods.
    """

    def __init__(self, wrapper: 'WorkerTaskWrapper', instance: object):
        self._wrapper = wrapper
        self._instance = instance
        self._pool: Optional['WorkerPool'] = None

    def __call__(self, *args, **kwargs):
        """
        Synchronous call: run the wrapped method immediately.
        """
        return self._wrapper.run(self._instance, *args, **kwargs)

    def async_call(self, *args, **kwargs) -> str:
        """
        Submit the wrapped method to the worker pool and return a task id.
        """
        pool = self._pool or WorkerPool.default_pool()
        task_id = pool.submit(self._wrapper, self._instance, *args, **kwargs)
        return task_id

    def submit(self, *args, **kwargs) -> str:
        """
        Alias for async_call.
        """
        return self.async_call(*args, **kwargs)

    def run_and_wait(self, *args, timeout: Optional[float] = None, **kwargs):
        """
        Submit the task and wait for the result.
        """
        task_id = self.async_call(*args, **kwargs)
        pool = self._pool or WorkerPool.default_pool()
        return pool.get_result(task_id, timeout=timeout)

    def set_pool(self, pool: 'WorkerPool'):
        """
        Set the worker pool to use for this method.
        """
        self._pool = pool

    def shutdown_default_pool(self):
        """
        Shut down the default pool if this method is using it.
        """
        if self._pool is None:
            pool = WorkerPool.default_pool()
            pool.shutdown()

    def __getattr__(self, name: str) -> Any:
        """
        Delegate attribute access to the wrapped instance.
        """
        return getattr(self._instance, name)
