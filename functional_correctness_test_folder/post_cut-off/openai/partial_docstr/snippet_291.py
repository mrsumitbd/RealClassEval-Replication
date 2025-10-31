
class ProgressScope:
    """
    A lightweight progress tracker that forwards progress updates to an
    MCPContext instance.  The context is expected to expose at least a
    ``set_progress`` method or a ``progress`` attribute.  If the context
    provides additional hooks (e.g. ``set_description`` or
    ``set_progress_total``) they are used when available.
    """

    def __init__(self, context: 'MCPContext', total: int, description: str):
        """
        Initialize a progress scope.

        Args:
            context: The parent MCPContext
            total: Total number of steps
            description: Description of the operation
        """
        self.context = context
        self.total = max(0, int(total))
        self.description = description
        self.current = 0

        # Inform the context about the new scope if it supports it
        if hasattr(context, "set_description"):
            try:
                context.set_description(description)
            except Exception:
                pass

        if hasattr(context, "set_progress_total"):
            try:
                context.set_progress_total(self.total)
            except Exception:
                pass

        # Initialise progress
        self.set_progress(0)

    def update(self, step: int = 1) -> None:
        """
        Increment the progress by ``step`` and forward the update to the
        context.  The progress is clamped to the total.
        """
        if step <= 0:
            return
        self.current += step
        if self.current > self.total:
            self.current = self.total
        self.set_progress(self.current)

    def set_progress(self, current: int) -> None:
        """
        Set the progress to an explicit value and forward it to the context.
        The value is clamped between 0 and ``total``.
        """
        current = max(0, min(int(current), self.total))
        self.current = current

        # Forward to the context
        if hasattr(self.context, "set_progress"):
            try:
                self.context.set_progress(current)
            except Exception:
                # Fallback to attribute assignment
                setattr(self.context, "progress", current)
        else:
            setattr(self.context, "progress", current)
