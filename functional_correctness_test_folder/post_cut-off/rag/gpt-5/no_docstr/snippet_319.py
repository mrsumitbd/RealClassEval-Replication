from __future__ import annotations

import threading
import time
import traceback
import uuid
from concurrent.futures import Future, ThreadPoolExecutor
from typing import Any, Callable, Dict, Optional


class TaskManager:
    '''Manages background tasks using a thread pool.'''

    def __init__(self, max_workers: Optional[int] = None):
        '''Initializes the TaskManager and the thread pool executor.'''
        self._executor = ThreadPoolExecutor(max_workers=max_workers)
        self._tasks: Dict[str, Dict[str, Any]] = {}
        self._futures: Dict[str, Future] = {}
        self._lock = threading.RLock()
        self._shutdown = False

    def _update_task(self, task_id: str, status: str, message: str, result: Optional[Any] = None):
        '''Helper function to update the status of a task.'''
        with self._lock:
            task = self._tasks.get(task_id)
            if not task:
                return
            task['status'] = status
            task['message'] = message
            task['updated_at'] = time.time()
            if result is not None:
                task['result'] = result

    def _task_done_callback(self, task_id: str, future: Future):
        '''Callback function executed when a task completes.'''
        try:
            if future.cancelled():
                self._update_task(task_id, 'cancelled',
                                  'Task was cancelled.', None)
                return
            exc = future.exception()
            if exc is not None:
                tb = ''.join(traceback.format_exception(
                    type(exc), exc, exc.__traceback__))
                with self._lock:
                    task = self._tasks.get(task_id)
                    if task is not None:
                        task['exception'] = repr(exc)
                        task['traceback'] = tb
                self._update_task(task_id, 'failed', str(exc), None)
            else:
                result = future.result()
                self._update_task(task_id, 'completed',
                                  'Task completed successfully.', result)
        finally:
            with self._lock:
                self._futures.pop(task_id, None)
                task = self._tasks.get(task_id)
                if task is not None and task.get('status') in {'completed', 'failed', 'cancelled'}:
                    task['ended_at'] = time.time()
                    if 'started_at' in task:
                        task['duration'] = task['ended_at'] - \
                            task['started_at']

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
                    'TaskManager has been shut down; cannot submit new tasks.')
            task_id = uuid.uuid4().hex
            now = time.time()
            self._tasks[task_id] = {
                'id': task_id,
                'status': 'queued',
                'message': 'Task has been submitted.',
                'result': None,
                'created_at': now,
                'updated_at': now,
            }

        def _wrapper():
            self._update_task(task_id, 'running', 'Task is running.')
            with self._lock:
                task = self._tasks.get(task_id)
                if task is not None and 'started_at' not in task:
                    task['started_at'] = time.time()
            return target_function(*args, **kwargs)

        try:
            future = self._executor.submit(_wrapper)
        except RuntimeError as e:
            # Executor has been shut down between check and submit
            self._update_task(task_id, 'failed',
                              f'Failed to submit task: {e}', None)
            raise RuntimeError(
                'Shutdown has been initiated; cannot submit task.') from e

        with self._lock:
            self._futures[task_id] = future
        future.add_done_callback(
            lambda f, tid=task_id: self._task_done_callback(tid, f))
        return task_id

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
            return dict(task) if task is not None else None

    def shutdown(self):
        '''Shuts down the thread pool and waits for all tasks to complete.'''
        with self._lock:
            self._shutdown = True
        self._executor.shutdown(wait=True)
