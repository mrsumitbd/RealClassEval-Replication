from typing import Optional, Any, Callable, Dict
from concurrent.futures import ThreadPoolExecutor, Future
import threading
import time
import uuid
import traceback
import logging


class TaskManager:
    '''Manages background tasks using a thread pool.'''

    def __init__(self, max_workers: Optional[int] = None):
        '''Initializes the TaskManager and the thread pool executor.'''
        self._executor = ThreadPoolExecutor(max_workers=max_workers)
        self._tasks: Dict[str, Dict[str, Any]] = {}
        self._lock = threading.RLock()
        self._shutdown = False
        self._logger = logging.getLogger(__name__)

    def _update_task(self, task_id: str, status: str, message: str, result: Optional[Any] = None):
        '''Helper function to update the status of a task.'''
        now = time.time()
        with self._lock:
            entry = self._tasks.get(task_id)
            if entry is None:
                entry = {'task_id': task_id, 'created_at': now}
                self._tasks[task_id] = entry
            entry['status'] = status
            entry['message'] = message
            entry['result'] = result
            entry['updated_at'] = now

    def _task_done_callback(self, task_id: str, future: Future):
        '''Callback function executed when a task completes.'''
        try:
            if future.cancelled():
                self._update_task(task_id, 'CANCELLED',
                                  'Task was cancelled', None)
                return

            exc = future.exception()
            if exc is not None:
                tb = ''.join(traceback.format_exception(
                    type(exc), exc, exc.__traceback__))
                with self._lock:
                    entry = self._tasks.get(task_id) or {'task_id': task_id}
                    self._tasks[task_id] = entry
                    entry['status'] = 'FAILED'
                    entry['message'] = str(exc)
                    entry['error'] = repr(exc)
                    entry['traceback'] = tb
                    entry['result'] = None
                    entry['updated_at'] = time.time()
                return

            result = future.result()
            self._update_task(task_id, 'COMPLETED',
                              'Task completed successfully', result)
        except Exception as e:
            self._logger.exception(
                'Error in task done callback for %s: %s', task_id, e)

    def run_task(self, target_function: Callable, *args: Any, **kwargs: Any) -> str:
        '''
        Submits a function to be run in the background.
        Args:
            target_function: The function to execute.
            *args: Positional arguments for the target function.
            **kwargs: Keyword arguments for the target function.
        Returns:
            The ID of the created task.
        Raises:
            RuntimeError: If shutdown has been initiated.
        '''
        if self._shutdown:
            raise RuntimeError(
                'TaskManager shutdown has been initiated; cannot run new tasks.')

        task_id = uuid.uuid4().hex
        now = time.time()
        with self._lock:
            self._tasks[task_id] = {
                'task_id': task_id,
                'status': 'SUBMITTED',
                'message': 'Task submitted',
                'result': None,
                'created_at': now,
                'updated_at': now,
            }

        def task_wrapper(*a: Any, **k: Any) -> Any:
            self._update_task(task_id, 'RUNNING', 'Task is running')
            return target_function(*a, **k)

        future = self._executor.submit(task_wrapper, *args, **kwargs)
        with self._lock:
            self._tasks[task_id]['future'] = future
        future.add_done_callback(
            lambda f, tid=task_id: self._task_done_callback(tid, f))
        return task_id

    def get_task(self, task_id: str) -> Optional[Dict[str, Any]]:
        '''
        Retrieves the status of a task.
        Args:
            task_id: The ID of the task to retrieve.
        Returns:
            The task details or None if not found.
        '''
        with self._lock:
            entry = self._tasks.get(task_id)
            if entry is None:
                return None
            data = dict(entry)
            data.pop('future', None)
            return data

    def shutdown(self):
        '''Shuts down the thread pool and waits for all tasks to complete.'''
        self._shutdown = True
        self._executor.shutdown(wait=True)
