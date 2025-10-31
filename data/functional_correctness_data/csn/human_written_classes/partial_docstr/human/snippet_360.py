from threading import BoundedSemaphore, Thread
from queue import Queue

class ThreadPool:
    """ Pool of threads consuming tasks from a queue """
    _results_queue: Queue
    _exceptions_queue: Queue
    _tasks_queue: Queue
    _sem: BoundedSemaphore
    _num_threads: int

    def __init__(self, num_threads: int):
        self._results_queue = Queue()
        self._exceptions_queue = Queue()
        self._tasks_queue = Queue()
        self._sem = BoundedSemaphore(num_threads)
        self._num_threads = num_threads

    def add_task(self, func, *args, **kargs):
        """
        Add a task to the queue. Calling this function can block
        until workers have a room for processing new tasks. Blocking
        the caller also prevents the latter from allocating a lot of
        memory while workers are still busy running their assigned tasks.
        """
        self._sem.acquire()
        cleanup_func = self._sem.release
        self._tasks_queue.put((func, args, kargs, cleanup_func))

    def start_parallel(self):
        """ Prepare threads to run tasks"""
        for _ in range(self._num_threads):
            Worker(self._tasks_queue, self._results_queue, self._exceptions_queue)

    def result(self) -> Queue:
        """ Stop threads and return the result of all called tasks """
        for _ in range(self._num_threads):
            self._tasks_queue.put(None)
        self._tasks_queue.join()
        if not self._exceptions_queue.empty():
            raise self._exceptions_queue.get()
        return self._results_queue