
from concurrent.futures import ThreadPoolExecutor, Future
from typing import Optional, Any, Callable, Dict
import threading
import uuid


class TaskManager:
    '''Manages background tasks using a thread pool.'''

    def __init__(self, max_workers: Optional[int] = None):
        '''Initializes the TaskManager and the thread pool executor.'''
        self.executor = ThreadPoolExecutor(max_workers=max_workers)
        self.tasks: Dict[str, Dict[str, Any]] = {}
        self.lock = threading.Lock()

    def _update_task(self, task_id: str, status: str, message: str, result: Optional[Any] = None):
        with self.lock:
            if task_id in self.tasks:
                self.tasks[task_id]['status'] = status
                self.tasks[task_id]['message'] = message
                if result is not None:
                    self.tasks[task_id]['result'] = result

    def _task_done_callback(self, task_id: str, future: Future):
        '''Callback function executed when a task completes.'''
        try:
            result = future.result()
            self._update_task(task_id, 'completed',
                              'Task completed successfully.', result)
        except Exception as e:
            self._update_task(task_id, 'failed', f'Task failed: {e}', None)

    def run_task(self, target_function: Callable, *args: Any, **kwargs: Any) -> str:
        task_id = str(uuid.uuid4())
        with self.lock:
            self.tasks[task_id] = {
                'status': 'running',
                'message': 'Task is running.',
                'result': None
            }
        future = self.executor.submit(target_function, *args, **kwargs)
        future.add_done_callback(
            lambda fut, tid=task_id: self._task_done_callback(tid, fut))
        return task_id

    def get_task(self, task_id: str) -> Optional[Dict[str, Any]]:
        with self.lock:
            return self.tasks.get(task_id, None)

    def shutdown(self):
        self.executor.shutdown(wait=True)
