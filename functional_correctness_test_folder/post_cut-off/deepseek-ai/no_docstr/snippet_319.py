
from typing import Optional, Any, Dict, Callable
from concurrent.futures import Future, ThreadPoolExecutor
import uuid
from threading import Lock


class TaskManager:

    def __init__(self, max_workers: Optional[int] = None):
        self._executor = ThreadPoolExecutor(max_workers=max_workers)
        self._tasks: Dict[str, Dict[str, Any]] = {}
        self._lock = Lock()

    def _update_task(self, task_id: str, status: str, message: str, result: Optional[Any] = None):
        with self._lock:
            if task_id in self._tasks:
                self._tasks[task_id].update({
                    'status': status,
                    'message': message,
                    'result': result
                })

    def _task_done_callback(self, task_id: str, future: Future):
        try:
            result = future.result()
            self._update_task(task_id, 'completed',
                              'Task completed successfully', result)
        except Exception as e:
            self._update_task(task_id, 'failed',
                              f'Task failed with error: {str(e)}')

    def run_task(self, target_function: Callable, *args: Any, **kwargs: Any) -> str:
        task_id = str(uuid.uuid4())
        with self._lock:
            self._tasks[task_id] = {
                'status': 'pending',
                'message': 'Task is pending execution',
                'result': None
            }
        future = self._executor.submit(target_function, *args, **kwargs)
        future.add_done_callback(
            lambda f: self._task_done_callback(task_id, f))
        return task_id

    def get_task(self, task_id: str) -> Optional[Dict[str, Any]]:
        with self._lock:
            return self._tasks.get(task_id, None)

    def shutdown(self):
        self._executor.shutdown(wait=True)
