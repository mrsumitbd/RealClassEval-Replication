from threading import Lock, Thread
import ctypes
from module.logger import logger

class WorkerThread:

    def __init__(self, thread_pool):
        """
        Args:
            thread_pool (WorkerPool):
        """
        self.job: 'Job | None' = None
        self.thread_pool = thread_pool
        self.worker_lock = Lock()
        self.worker_lock.acquire()
        self.default_name = f'Alasio thread {next(name_counter)}'
        self.thread = Thread(target=self._work, name=self.default_name, daemon=True)
        self.thread.start()

    def __repr__(self):
        return f'{self.__class__.__name__}({self.default_name})'

    def _handle_job(self) -> None:
        job = self.job
        del self.job
        func, args, kwargs = job.func_args_kwargs
        result = capture(func, *args, **kwargs)
        self.thread_pool.idle_workers[self] = None
        self.thread_pool.release_full_lock()
        if isinstance(result, Error) and isinstance(result.error, _JobKill):
            pass
        else:
            with job.put_lock:
                job.queue.append(result)
                del job.worker
                job.notify_get.release()

    def _work(self) -> None:
        while True:
            if self.worker_lock.acquire(timeout=WorkerPool.IDLE_TIMEOUT):
                self._handle_job()
            else:
                try:
                    del self.thread_pool.idle_workers[self]
                except KeyError:
                    self.thread_pool.release_full_lock()
                    continue
                else:
                    del self.thread_pool.all_workers[self]
                    self.thread_pool.release_full_lock()
                    return

    def kill(self):
        """
        Yes, it's unsafe to kill a thread, but what else can you do
        if a single job function get blocked.
        This method should be protected by `job.put_lock` to prevent
        race condition with `_handle_job()`.

        Returns:
            bool: If success to kill the thread
        """
        thread_id = ctypes.c_long(self.thread.ident)
        res = ctypes.pythonapi.PyThreadState_SetAsyncExc(thread_id, ctypes.py_object(_JobKill))
        if res <= 1:
            self.thread_pool.all_workers.pop(self, None)
            self.thread_pool.release_full_lock()
            return True
        else:
            try:
                job = self.job
            except AttributeError:
                job = None
            logger.error(f'Failed to kill thread {self.thread.ident} from job {job}')
            ctypes.pythonapi.PyThreadState_SetAsyncExc(thread_id, 0)
            return False