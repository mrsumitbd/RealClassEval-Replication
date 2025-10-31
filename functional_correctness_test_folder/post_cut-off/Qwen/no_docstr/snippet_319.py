
from concurrent.futures import ThreadPoolExecutor, Future
from typing import Optional, Any, Callable, Dict
import uuid


class TaskManager:

    def __init__(self, max_workers: Optional[int] = None):
        self.executor = ThreadPoolExecutor(max_workers=max_workers)
        self.tasks = {}

    def _update_task(self, task_id: str, status: str, message: str, result: Optional[Any] = None):
        if task_id in self.tasks:
            self.tasks[task_id].update({
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
        self.tasks[task_id] = {
            'status': 'running',
            'message': 'Task is running',
            'result': None
        }
        future = self.executor.submit(target_function, *args, **kwargs)
        future.add_done_callback(
            lambda f: self._task_done_callback(task_id, f))
        return task_id

    def get_task(self, task_id: str) -> Optional[Dict[str, Any]]:
        return self.tasks.get(task_id)

    def shutdown(self):
        self.executor.shutdown(wait=True)
