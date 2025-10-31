class ProgressScope:

    def __init__(self, context: 'MCPContext', total: int, description: str):
        '''
        Initialize a progress scope.
        Args:
            context: The parent MCPContext
            total: Total number of steps
            description: Description of the operation
        '''
        if total is None or total < 0:
            raise ValueError("total must be a non-negative integer")
        self.context = context
        self.total = int(total)
        self.description = str(description) if description is not None else ""
        self.current = 0
        self._closed = False

        # Thread-safety for concurrent updates
        try:
            import threading
            self._lock = threading.Lock()
        except Exception:
            # Fallback if threading is unavailable
            class _DummyLock:
                def __enter__(self): return None
                def __exit__(self, *args): return False
            self._lock = _DummyLock()

        # Initial notify
        self._notify()

    def update(self, step: int = 1) -> None:
        if step is None:
            step = 1
        if not isinstance(step, int):
            try:
                step = int(step)
            except Exception:
                raise TypeError("step must be an integer")
        with self._lock:
            if self._closed:
                return
            self.current += step
            if self.current < 0:
                self.current = 0
            if self.total >= 0 and self.current > self.total:
                self.current = self.total
            if self.total > 0 and self.current >= self.total:
                self._closed = True
        self._notify()

    def set_progress(self, current: int) -> None:
        if current is None:
            current = 0
        if not isinstance(current, int):
            try:
                current = int(current)
            except Exception:
                raise TypeError("current must be an integer")
        with self._lock:
            if self._closed:
                return
            if current < 0:
                current = 0
            if self.total >= 0 and current > self.total:
                current = self.total
            self.current = current
            if self.total > 0 and self.current >= self.total:
                self._closed = True
        self._notify()

    def _notify(self) -> None:
        data = {
            "description": self.description,
            "total": self.total,
            "current": self.current,
            "remaining": None if self.total <= 0 else max(self.total - self.current, 0),
            "done": bool(self.total > 0 and self.current >= self.total),
            "percent": None if self.total <= 0 else (self.current / self.total if self.total else None),
        }

        ctx = self.context

        # Try common method names; ignore if not present or raises
        for name in (
            "report_progress",
            "on_progress",
            "on_progress_update",
            "update_progress",
            "progress",
            "set_progress",
        ):
            try:
                fn = getattr(ctx, name, None)
                if callable(fn):
                    fn(data)
                    return
            except Exception:
                # Swallow exceptions from context hooks to avoid breaking progress updates
                pass
        # As a last resort, try attribute assignment for simple contexts
        try:
            setattr(ctx, "last_progress", data)
        except Exception:
            pass
