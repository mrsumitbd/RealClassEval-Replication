class ProgressScope:
    def __init__(self, context: 'MCPContext', total: int, description: str):
        self.context = context
        self.total = max(int(total), 0)
        self.description = description
        self.current = 0
        self._completed = False
        self._started = False
        self._notify_start()
        self._notify_progress()

    def update(self, step: int = 1) -> None:
        self.set_progress(self.current + int(step))

    def set_progress(self, current: int) -> None:
        current = int(current)
        if current < 0:
            current = 0
        if self.total > 0:
            current = min(current, self.total)
        self.current = current
        self._notify_progress()
        if self.total > 0 and self.current >= self.total and not self._completed:
            self._completed = True
            self._notify_end()

    # Internal helpers

    def _notify_start(self) -> None:
        if self._started:
            return
        self._started = True
        self._call_if_exists(
            [
                "begin_progress",
                "progress_begin",
                "on_progress_start",
                "start_progress",
            ],
            self.total,
            self.description,
        )

    def _notify_progress(self) -> None:
        percent = None
        if self.total > 0:
            percent = self.current / self.total
        # Try common method names
        if not self._call_if_exists(
            [
                "report_progress",
                "progress",
                "on_progress",
                "update_progress",
            ],
            self.current,
            self.total,
            self.description,
            percent,
        ):
            # Try attribute-style progress reporter
            reporter = getattr(self.context, "progress", None)
            if reporter and hasattr(reporter, "update") and callable(reporter.update):
                try:
                    reporter.update(self.current, self.total,
                                    self.description, percent)
                except Exception:
                    pass

    def _notify_end(self) -> None:
        self._call_if_exists(
            [
                "end_progress",
                "progress_end",
                "on_progress_end",
                "complete_progress",
                "on_progress_complete",
            ],
            self.current,
            self.total,
            self.description,
        )

    def _call_if_exists(self, names, *args):
        called = False
        for name in names:
            func = getattr(self.context, name, None)
            if callable(func):
                try:
                    func(*args)
                    called = True
                except Exception:
                    pass
        return called
