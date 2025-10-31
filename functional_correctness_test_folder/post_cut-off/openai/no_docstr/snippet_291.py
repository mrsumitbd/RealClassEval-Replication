
class ProgressScope:
    """
    A lightweight progress tracker that reports progress to an optional
    ``MCPContext`` instance.  The context is expected to expose either a
    ``set_progress`` or ``update_progress`` method that accepts the current
    progress, the total amount, and an optional description.
    """

    def __init__(self, context: 'MCPContext', total: int, description: str):
        self.context = context
        self.total = max(0, int(total))
        self.description = description
        self.current = 0
        self._report()

    # ------------------------------------------------------------------
    # Context‑manager protocol (optional)
    # ------------------------------------------------------------------
    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc, tb):
        # Ensure the progress is marked as complete when exiting the block
        self.current = self.total
        self._report()

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------
    def update(self, step: int = 1) -> None:
        """Increment the progress by *step* and report."""
        self.current += int(step)
        if self.current > self.total:
            self.current = self.total
        self._report()

    def set_progress(self, current: int) -> None:
        """Set the progress to *current* and report."""
        self.current = int(current)
        if self.current > self.total:
            self.current = self.total
        self._report()

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------
    def _report(self) -> None:
        """
        Attempt to report the current progress to the context.  The method
        signature of the context is not strictly defined, so we try a few
        common patterns.
        """
        if not hasattr(self.context, "__dict__"):
            # If the context is a simple object without attributes, skip.
            return

        # Preferred: set_progress(current, total, description)
        if hasattr(self.context, "set_progress"):
            try:
                self.context.set_progress(
                    self.current, self.total, self.description)
                return
            except TypeError:
                pass

        # Fallback: set_progress(current, total)
        if hasattr(self.context, "set_progress"):
            try:
                self.context.set_progress(self.current, self.total)
                return
            except TypeError:
                pass

        # Alternative: update_progress(current, total, description)
        if hasattr(self.context, "update_progress"):
            try:
                self.context.update_progress(
                    self.current, self.total, self.description)
                return
            except TypeError:
                pass

        # Fallback: update_progress(current, total)
        if hasattr(self.context, "update_progress"):
            try:
                self.context.update_progress(self.current, self.total)
                return
            except TypeError:
                pass

        # If none of the above work, silently ignore.
        return
