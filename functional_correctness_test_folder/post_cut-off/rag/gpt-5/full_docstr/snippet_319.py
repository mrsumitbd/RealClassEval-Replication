from concurrent.futures import ThreadPoolExecutor, Future
from typing import Optional, Any, Callable, Dict
import threading
import time
import uuid
import traceback
from functools import partial


class TaskManager:
    """Manages background tasks using a thread pool."""

    def __init__(self, max_workers: Optional[int] = None):
        """Initializes the TaskManager and the thread pool executor."""
        self._executor = ThreadPoolExecutor(max_workers=max_workers)
        self._tasks: Dict[str, Dict[str, Any]] = {}
        self._lock = threading.RLock()
        self._shutdown = False

    def _update_task(self, task_id: str, status: str, message: str, result: Optional[Any] = None):
        """Helper function to update the status of a task."""
        with self._lock:
            task = self._tasks.get(task_id)
            if not task:
                return
            task["status"] = status
            task["message"] = message
            if result is not None:
                task["result"] = result
            task["updated_at"] = time.time()

    def _task_done_callback(self, task_id: str, future: Future):
        """Callback function executed when a task completes."""
        finished_at = time.time()
        try:
            if future.cancelled():
                self._update_task(task_id, "cancelled", "Task was cancelled")
                with self._lock:
                    task = self._tasks.get(task_id)
                    if task is not None:
                        task["finished_at"] = finished_at
                        task["duration"] = finished_at - \
                            task.get("started_at", task.get(
                                "created_at", finished_at))
                return

            exc = future.exception()
            if exc is None:
                result = future.result()
                self._update_task(task_id, "completed",
                                  "Task completed successfully", result)
                with self._lock:
                    task = self._tasks.get(task_id)
                    if task is not None:
                        task["finished_at"] = finished_at
                        task["duration"] = finished_at - \
                            task.get("started_at", task.get(
                                "created_at", finished_at))
            else:
                tb = "".join(traceback.format_exception(
                    type(exc), exc, exc.__traceback__))
                with self._lock:
                    task = self._tasks.get(task_id)
                    if task is not None:
                        task["error"] = str(exc)
                        task["traceback"] = tb
                self._update_task(task_id, "failed", str(exc))
                with self._lock:
                    task = self._tasks.get(task_id)
                    if task is not None:
                        task["finished_at"] = finished_at
                        task["duration"] = finished_at - \
                            task.get("started_at", task.get(
                                "created_at", finished_at))
        except Exception as err:
            tb = "".join(traceback.format_exception(
                type(err), err, err.__traceback__))
            with self._lock:
                task = self._tasks.get(task_id)
                if task is not None:
                    task["error"] = str(err)
                    task["traceback"] = tb
            self._update_task(task_id, "failed",
                              f"Task callback encountered an error: {err}")
            with self._lock:
                task = self._tasks.get(task_id)
                if task is not None:
                    task["finished_at"] = finished_at
                    task["duration"] = finished_at - \
                        task.get("started_at", task.get(
                            "created_at", finished_at))

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
                "TaskManager is shutting down; cannot accept new tasks.")

        task_id = uuid.uuid4().hex
        created_at = time.time()
        with self._lock:
            self._tasks[task_id] = {
                "id": task_id,
                "status": "queued",
                "message": "Task queued",
                "result": None,
                "error": None,
                "traceback": None,
                "created_at": created_at,
                "updated_at": created_at,
                "started_at": None,
                "finished_at": None,
                "duration": None,
                "function": getattr(target_function, "__name__", str(target_function)),
            }

        def _wrapped():
            with self._lock:
                task = self._tasks.get(task_id)
                if task is not None:
                    task["started_at"] = time.time()
            self._update_task(task_id, "running", "Task started")
            return target_function(*args, **kwargs)

        future = self._executor.submit(_wrapped)
        with self._lock:
            self._tasks[task_id]["_future"] = future  # internal reference

        future.add_done_callback(partial(self._task_done_callback, task_id))
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
            if task is None:
                return None
            data = dict(task)
            data.pop("_future", None)
            return data

    def shutdown(self):
        """Shuts down the thread pool and waits for all tasks to complete."""
        self._shutdown = True
        try:
            self._executor.shutdown(wait=True)
        finally:
            with self._lock:
                for t in self._tasks.values():
                    fut: Optional[Future] = t.get("_future")
                    if fut is not None and fut.cancelled():
                        t["status"] = "cancelled"
                        t["message"] = "Task was cancelled"
                        t["finished_at"] = time.time()
                        t["duration"] = t["finished_at"] - \
                            (t.get("started_at") or t.get(
                                "created_at") or t["finished_at"])
                # Optionally clear internal future references
                for t in self._tasks.values():
                    t.pop("_future", None)
