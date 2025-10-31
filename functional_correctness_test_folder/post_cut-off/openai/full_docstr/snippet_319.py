
from __future__ import annotations

import uuid
import threading
from concurrent.futures import ThreadPoolExecutor, Future
from typing import Any, Callable, Dict, Optional


class TaskManager:
    '''Manages background tasks using a thread pool.'''

    def __init__(self, max_workers: Optional[int] = None):
        '''Initializes the TaskManager and the thread pool executor.'''
        self._executor = ThreadPoolExecutor(max_workers=max_workers)
        self._tasks: Dict[str, Dict[str, Any]] = {}
        self._lock = threading.Lock()
        self._shutdown = False

    def _update_task(self, task_id: str, status: str, message: str, result: Optional[Any] = None):
        '''Helper function to update the status of a task.'''
        with self._lock:
            task = self._tasks.get(task_id)
            if task is not None:
                task['status'] = status
                task['message'] = message
                if result is not None:
                    task['result'] = result

    def _task_done_callback(self, task_id: str, future: Future):
        '''Callback function executed when a task completes.'''
        try:
            result = future.result()
            self._update_task(task_id, 'completed',
                              'Task finished successfully', result)
        except Exception as exc:
            self._update_task(task_id, 'failed',
                              f'Task raised exception: {exc}')

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
                'TaskManager has been shut down; cannot submit new tasks.')

        task_id = str(uuid.uuid4())
        future = self._executor.submit(target_function, *args, **kwargs)

        with self._lock:
            self._tasks[task_id] = {
                'status': 'running',
                'message': 'Task started',
                'result': None,
                'future': future,
            }

        # Attach callback
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
            # Return a shallow copy without the future object
            return {
                'status': task['status'],
                'message': task['message'],
                'result': task['result'],
            }

    def shutdown(self):
        '''Shuts down the thread pool and waits for all tasks to complete.'''
        with self._lock:
            self._shutdown = True
        self._executor.shutdown(wait=True)
