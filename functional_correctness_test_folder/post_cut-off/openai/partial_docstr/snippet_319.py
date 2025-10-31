
from concurrent.futures import ThreadPoolExecutor, Future
from typing import Any, Callable, Dict, Optional
import uuid
import threading


class TaskManager:
    '''Manages background tasks using a thread pool.'''

    def __init__(self, max_workers: Optional[int] = None):
        '''Initializes the TaskManager and the thread pool executor.'''
        self._executor = ThreadPoolExecutor(max_workers=max_workers)
        self._tasks: Dict[str, Dict[str, Any]] = {}
        self._lock = threading.Lock()

    def _update_task(self, task_id: str, status: str, message: str, result: Optional[Any] = None):
        with self._lock:
            task = self._tasks.get(task_id)
            if task is not None:
                task['status'] = status
                task['message'] = message
                task['result'] = result

    def _task_done_callback(self, task_id: str, future: Future):
        '''Callback function executed when a task completes.'''
        try:
            result = future.result()
            self._update_task(task_id, 'completed',
                              'Task finished successfully', result)
        except Exception as exc:
            self._update_task(task_id, 'failed',
                              f'Task raised exception: {exc}', None)

    def run_task(self, target_function: Callable, *args: Any, **kwargs: Any) -> str:
        '''Submits a task to the thread pool and returns its unique ID.'''
        task_id = uuid.uuid4().hex
        with self._lock:
            self._tasks[task_id] = {
                'status': 'queued',
                'message': 'Task queued',
                'result': None,
                'future': None,
            }
        future = self._executor.submit(target_function, *args, **kwargs)
        with self._lock:
            self._tasks[task_id]['future'] = future
        future.add_done_callback(
            lambda fut, tid=task_id: self._task_done_callback(tid, fut))
        return task_id

    def get_task(self, task_id: str) -> Optional[Dict[str, Any]]:
        '''Returns the current state of the task with the given ID.'''
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
        '''Shuts down the thread pool executor.'''
        self._executor.shutdown(wait=True)
