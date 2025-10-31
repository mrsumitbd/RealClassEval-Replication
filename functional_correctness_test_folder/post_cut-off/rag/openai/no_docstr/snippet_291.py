
class ProgressScope:
    '''Scope for tracking progress of an operation.'''

    def __init__(self, context: 'MCPContext', total: int, description: str):
        '''
        Initialize a progress scope.
        Args:
            context: The parent MCPContext
            total: Total number of steps
            description: Description of the operation
        '''
        self.context = context
        self.total = max(1, int(total))
        self.description = description
        self.current = 0

        # Try to initialise a progress bar if the context provides one
        progress = getattr(context, 'progress', None)
        if progress is not None:
            try:
                # Some progress objects expose a `start` or `__init__` that accepts total and description
                if hasattr(progress, 'start'):
                    progress.start(self.total, self.description)
                else:
                    # If the progress object is already initialised, just update it
                    progress.update(self.current, self.total)
            except Exception:
                # Silently ignore any failure – progress is optional
                pass

    def update(self, step: int = 1) -> None:
        '''
        Update progress by a number of steps.
        Args:
            step: Number of steps to add to progress
        '''
        self.current += int(step)
        if self.current > self.total:
            self.current = self.total
        self._sync_progress()

    def set_progress(self, current: int) -> None:
        '''
        Set progress to a specific value.
        Args:
            current: Current progress value
        '''
        self.current = int(current)
        if self.current > self.total:
            self.current = self.total
        if self.current < 0:
            self.current = 0
        self._sync_progress()

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------
    def _sync_progress(self) -> None:
        """Synchronise the internal progress counter with the context's progress object."""
        progress = getattr(self.context, 'progress', None)
        if progress is not None:
            try:
                # Most progress objects expose an `update` method that accepts current and total
                progress.update(self.current, self.total)
            except Exception:
                # If the progress object doesn't support this, ignore
                pass
