
import concurrent.futures
import threading
import uuid
import time
from typing import Any, Callable, Dict, Optional


class TaskManager:
    """Manages background tasks using a thread pool."""

    def __init__(self, max_workers: Optional[int] = None):
        """Initializes the TaskManager and the thread pool executor."""
        self._executor = concurrent.futures.ThreadPoolExecutor(
            max_workers=max_workers)
        self._tasks: Dict[str, Dict[str, Any]] = {}
        self._lock = threading.Lock()
        self._shutdown = False

    def _update_task(
        self,
        task_id: str,
        status: str,
        message: str,
        result: Optional[Any] = None,
    ) -> None:
        """Helper function to update the status of a task."""
        with self._lock:
            task = self._tasks.get(task_id)
            if task is None:
                return
            task["status"] = status
            task["message"] = message
            if result is not None:
                task["result"] = result
            if status in ("completed", "failed"):
                task["end_time"] = time.time()

    def _task_done_callback(self, task_id: str, future: concurrent.futures.Future) -> None:
        """Callback function executed when a task completes."""
        try:
            result = future.result()
            self._update_task(task_id, "completed",
                              "Task finished successfully", result)
        except Exception as exc:
            self._update_task(task_id, "failed",
                              f"Task raised exception: {exc}")

    def run_task(self, target_function: Callable, *args: Any, **kwargs: Any) -> str:
        """
        Submits a function to be run in the background.
        Args:
            target_function: The function to execute.
            *args: Positional arguments for the target function.
            **kwargs: Keyword arguments for the target function.
        Returns:
            The ID of the created task.
        Raises:
            RuntimeError: If shutdown has been initiated.
        """
        if self._shutdown:
            raise RuntimeError(
                "TaskManager has been shut down; cannot submit new tasks.")
        task_id = str(uuid.uuid4())
        task_info: Dict[str, Any] = {
            "id": task_id,
            "status": "queued",
            "message": "Task queued",
            "result": None,
            "start_time": time.time(),
            "end_time": None,
        }
        with self._lock:
            self._tasks[task_id] = task_info
        future = self._executor.submit(target_function, *args, **kwargs)
        future.add_done_callback(
            lambda fut, tid=task_id: self._task_done_callback(tid, fut))
        return task_id

    def get_task(self, task_id: str) -> Optional[Dict[str, Any]]:
        """
        Retrieves the status of a task.
        Args:
            task_id: The ID of the task to retrieve.
        Returns:
            The task details or None if not found.
        """
        with self._lock:
            task = self._tasks.get(task_id)
            return dict(task) if task is not None else None

    def shutdown(self):
        """Shuts down the thread pool and waits for all tasks to complete."""
        self._shutdown = True
        self._executor.shutdown(wait=True)
