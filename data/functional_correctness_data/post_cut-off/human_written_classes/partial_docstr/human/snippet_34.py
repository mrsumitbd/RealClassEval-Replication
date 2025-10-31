from typing import Any, Callable, Coroutine, Generator, ParamSpec, TypeVar, cast
import time
import cloudpickle
import contextlib

class WorkerExtension:
    """Extension for running arbitrary functions on vLLM workers."""

    def run(self, pickled_func: bytes, *args: Any, **kwargs: Any) -> Any:
        func = cloudpickle.loads(pickled_func)
        token = _worker.set(cast(ExtendedWorker, self))
        try:
            return func(*args, **kwargs)
        finally:
            _worker.reset(token)

    @contextlib.contextmanager
    def time(self, name: str) -> Generator[None, None, None]:
        from vllm.v1.worker.gpu_worker import logger
        start_time = time.perf_counter()
        yield
        end_time = time.perf_counter()
        logger.info(f'{name}: {end_time - start_time:.2f} seconds')