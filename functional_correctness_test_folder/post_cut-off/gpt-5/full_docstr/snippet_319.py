from concurrent.futures import ThreadPoolExecutor, Future
from typing import Optional, Any, Callable, Dict
from threading import Lock
import uuid
import time


class TaskManager:
    '''Manages background tasks using a thread pool.'''

    def __init__(self, max_workers: Optional[int] = None):
        '''Initializes the TaskManager and the thread pool executor.'''
        self._executor = ThreadPoolExecutor(max_workers=max_workers)
        self._tasks: Dict[str, Dict[str, Any]] = {}
        self._lock = Lock()
        self._shutdown = False

    def _update_task(self, task_id: str, status: str, message: str, result: Optional[Any] = None):
        '''Helper function to update the status of a task.'''
        with self._lock:
            task = self._tasks.get(task_id)
            if not task:
                return
            task['status'] = status
            task['message'] = message
            task['result'] = result
            task['updated_at'] = time.time()

    def _task_done_callback(self, task_id: str, future: Future):
        '''Callback function executed when a task completes.'''
        try:
            if future.cancelled():
                self._update_task(task_id, 'cancelled',
                                  'Task was cancelled', None)
                return
            exc = future.exception()
            if exc is not None:
                self._update_task(task_id, 'failed', f'Error: {exc}', None)
                return
            result = future.result()
            self._update_task(task_id, 'completed',
                              'Task completed successfully', result)
        except Exception as e:
            self._update_task(task_id, 'failed', f'Callback error: {e}', None)

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
        with self._lock:
            if self._shutdown:
                raise RuntimeError(
                    'TaskManager has been shutdown; no new tasks can be submitted.')
            task_id = uuid.uuid4().hex
            self._tasks[task_id] = {
                'task_id': task_id,
                'status': 'queued',
                'message': 'Task queued',
                'result': None,
                'created_at': time.time(),
                'updated_at': time.time(),
                'future': None,
            }
        future = self._executor.submit(target_function, *args, **kwargs)
        with self._lock:
            self._tasks[task_id]['future'] = future
            self._tasks[task_id]['status'] = 'running'
            self._tasks[task_id]['message'] = 'Task is running'
            self._tasks[task_id]['updated_at'] = time.time()
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
            task = self._tasks.get(task_id)
            if task is None:
                return None
            data = dict(task)
            data.pop('future', None)
            return data

    def shutdown(self):
        '''Shuts down the thread pool and waits for all tasks to complete.'''
        with self._lock:
            if self._shutdown:
                return
            self._shutdown = True
        self._executor.shutdown(wait=True)
