
from concurrent.futures import ThreadPoolExecutor, Future
from typing import Any, Callable, Dict, Optional
import uuid
import threading


class TaskManager:
    def __init__(self, max_workers: Optional[int] = None):
        """
        Initialize the TaskManager with an optional maximum number of worker threads.
        """
        self._executor = ThreadPoolExecutor(max_workers=max_workers)
        self._tasks: Dict[str, Dict[str, Any]] = {}
        self._lock = threading.Lock()

    def _update_task(
        self,
        task_id: str,
        status: str,
        message: str,
        result: Optional[Any] = None,
    ):
        """
        Update the internal task record with the given status, message, and result.
        """
        with self._lock:
            if task_id in self._tasks:
                self._tasks[task_id].update(
                    {"status": status, "message": message, "result": result}
                )

    def _task_done_callback(self, task_id: str, future: Future):
        """
        Callback invoked when a submitted task completes.
        """
        try:
            result = future.result()
            self._update_task(task_id, "completed",
                              "Task finished successfully", result)
        except Exception as exc:
            self._update_task(task_id, "failed",
                              f"Task raised exception: {exc}", None)

    def run_task(self, target_function: Callable, *args: Any, **kwargs: Any) -> str:
        """
        Submit a task to the executor and return a unique task ID.
        """
        task_id = str(uuid.uuid4())
        with self._lock:
            self._tasks[task_id] = {
                "status": "pending",
                "message": "Task queued",
                "result": None,
            }
        future = self._executor.submit(target_function, *args, **kwargs)
        # Update status to running immediately after submission
        self._update_task(task_id, "running", "Task is running")
        future.add_done_callback(
            lambda f: self._task_done_callback(task_id, f))
        return task_id

    def get_task(self, task_id: str) -> Optional[Dict[str, Any]]:
        """
        Retrieve the current state of a task by its ID.
        """
        with self._lock:
            task = self._tasks.get(task_id)
            if task is not None:
                return dict(task)  # return a copy to avoid external mutation
            return None

    def shutdown(self):
        """
        Shut down the executor, waiting for all running tasks to finish.
        """
        self._executor.shutdown(wait=True)
