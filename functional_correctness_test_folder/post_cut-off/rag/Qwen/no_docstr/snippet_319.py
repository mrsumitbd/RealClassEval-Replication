
import threading
import uuid
from concurrent.futures import ThreadPoolExecutor, Future
from typing import Any, Callable, Dict, Optional


class TaskManager:
    '''Manages background tasks using a thread pool.'''

    def __init__(self, max_workers: Optional[int] = None):
        '''Initializes the TaskManager and the thread pool executor.'''
        self._executor = ThreadPoolExecutor(max_workers=max_workers)
        self._tasks: Dict[str, Dict[str, Any]] = {}
        self._lock = threading.Lock()

    def _update_task(self, task_id: str, status: str, message: str, result: Optional[Any] = None):
        '''Helper function to update the status of a task.'''
        with self._lock:
            if task_id in self._tasks:
                self._tasks[task_id].update({
                    'status': status,
                    'message': message,
                    'result': result
                })

    def _task_done_callback(self, task_id: str, future: Future):
        '''Callback function executed when a task completes.'''
        try:
            result = future.result()
            self._update_task(task_id, 'completed',
                              'Task completed successfully', result)
        except Exception as e:
            self._update_task(task_id, 'failed',
                              f'Task failed with error: {str(e)}')

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
        if self._executor._shutdown:
            raise RuntimeError("Shutdown has been initiated.")
        task_id = str(uuid.uuid4())
        with self._lock:
            self._tasks[task_id] = {
                'status': 'running',
                'message': 'Task is running',
                'result': None
            }
        future = self._executor.submit(target_function, *args, **kwargs)
        future.add_done_callback(
            lambda f: self._task_done_callback(task_id, f))
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
            return self._tasks.get(task_id)

    def shutdown(self):
        '''Shuts down the thread pool and waits for all tasks to complete.'''
        self._executor.shutdown(wait=True)
