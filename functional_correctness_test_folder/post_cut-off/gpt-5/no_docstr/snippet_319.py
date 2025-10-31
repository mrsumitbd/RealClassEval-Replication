from typing import Optional, Any, Dict, Callable
from concurrent.futures import ThreadPoolExecutor, Future
from uuid import uuid4
from threading import Lock
from datetime import datetime
import traceback as tb


class TaskManager:
    def __init__(self, max_workers: Optional[int] = None):
        self._executor = ThreadPoolExecutor(max_workers=max_workers)
        self._tasks: Dict[str, Dict[str, Any]] = {}
        self._lock = Lock()
        self._shutdown = False

    def _now(self) -> str:
        return datetime.utcnow().isoformat() + "Z"

    def _update_task(self, task_id: str, status: str, message: str, result: Optional[Any] = None):
        with self._lock:
            task = self._tasks.get(task_id)
            if not task:
                return
            task["status"] = status
            task["message"] = message
            if result is not None:
                task["result"] = result
            task["updated_at"] = self._now()

    def _task_done_callback(self, task_id: str, future: Future):
        try:
            result = future.result()
            self._update_task(task_id, "finished",
                              "Task completed successfully", result)
        except Exception as exc:
            exc_msg = f"{type(exc).__name__}: {exc}"
            tb_str = tb.format_exc()
            with self._lock:
                task = self._tasks.get(task_id)
                if task:
                    task["status"] = "failed"
                    task["message"] = "Task raised an exception"
                    task["error"] = exc_msg
                    task["traceback"] = tb_str
                    task["updated_at"] = self._now()

    def run_task(self, target_function: Callable, *args: Any, **kwargs: Any) -> str:
        if self._shutdown:
            raise RuntimeError(
                "TaskManager is shutdown; no new tasks can be submitted.")
        task_id = str(uuid4())
        created_at = self._now()
        with self._lock:
            self._tasks[task_id] = {
                "id": task_id,
                "status": "queued",
                "message": "Task is queued",
                "result": None,
                "error": None,
                "traceback": None,
                "created_at": created_at,
                "updated_at": created_at,
                "future": None,
            }

        def wrapper():
            self._update_task(task_id, "running", "Task started")
            return target_function(*args, **kwargs)

        future = self._executor.submit(wrapper)
        future.add_done_callback(
            lambda f, tid=task_id: self._task_done_callback(tid, f))
        with self._lock:
            if task_id in self._tasks:
                self._tasks[task_id]["future"] = future
        return task_id

    def get_task(self, task_id: str) -> Optional[Dict[str, Any]]:
        with self._lock:
            task = self._tasks.get(task_id)
            if not task:
                return None
            data = dict(task)
            data.pop("future", None)
            return data

    def shutdown(self):
        self._shutdown = True
        self._executor.shutdown(wait=True)
