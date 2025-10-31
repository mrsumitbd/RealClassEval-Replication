from typing import Optional, Any, Callable, Dict
from concurrent.futures import ThreadPoolExecutor, Future
import threading
import uuid
import traceback
from datetime import datetime


class TaskManager:
    '''Manages background tasks using a thread pool.'''

    def __init__(self, max_workers: Optional[int] = None):
        '''Initializes the TaskManager and the thread pool executor.'''
        self._executor = ThreadPoolExecutor(max_workers=max_workers)
        self._tasks: Dict[str, Dict[str, Any]] = {}
        self._futures: Dict[str, Future] = {}
        self._lock = threading.Lock()
        self._shutdown = False

    def _update_task(self, task_id: str, status: str, message: str, result: Optional[Any] = None):
        now = datetime.utcnow().isoformat() + "Z"
        with self._lock:
            task = self._tasks.get(task_id)
            if not task:
                return
            task['status'] = status
            task['message'] = message
            task['updated_at'] = now
            if result is not None:
                task['result'] = result
            if status in ('finished', 'failed', 'cancelled'):
                task['ended_at'] = now

    def _task_done_callback(self, task_id: str, future: Future):
        '''Callback function executed when a task completes.'''
        try:
            if future.cancelled():
                self._update_task(task_id, 'cancelled', 'Task was cancelled.')
                return
            result = future.result()
            self._update_task(task_id, 'finished',
                              'Task completed successfully.', result=result)
        except Exception as exc:
            tb = traceback.format_exc()
            with self._lock:
                task = self._tasks.get(task_id)
                if task is not None:
                    task['exception'] = exc
                    task['traceback'] = tb
            self._update_task(task_id, 'failed', f'Task failed: {exc}')

    def run_task(self, target_function: Callable, *args: Any, **kwargs: Any) -> str:
        if self._shutdown:
            raise RuntimeError(
                "TaskManager is shutdown; cannot submit new tasks.")
        task_id = str(uuid.uuid4())
        created = datetime.utcnow().isoformat() + "Z"

        def wrapper():
            self._update_task(task_id, 'running', 'Task started.')
            return target_function(*args, **kwargs)

        with self._lock:
            self._tasks[task_id] = {
                'id': task_id,
                'status': 'submitted',
                'message': 'Task submitted.',
                'result': None,
                'exception': None,
                'traceback': None,
                'created_at': created,
                'updated_at': created,
                'ended_at': None,
            }

        future = self._executor.submit(wrapper)
        with self._lock:
            self._futures[task_id] = future
        future.add_done_callback(
            lambda fut, tid=task_id: self._task_done_callback(tid, fut))
        return task_id

    def get_task(self, task_id: str) -> Optional[Dict[str, Any]]:
        with self._lock:
            task = self._tasks.get(task_id)
            if task is None:
                return None
            return dict(task)

    def shutdown(self):
        self._shutdown = True
        self._executor.shutdown(wait=True)
