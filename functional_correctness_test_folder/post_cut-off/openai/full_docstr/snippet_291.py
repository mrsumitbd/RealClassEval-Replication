
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
        self.total = max(0, int(total))
        self.description = description
        self.current = 0
        self._report()

    def _report(self) -> None:
        """Internal helper to report progress to the context."""
        # Prefer a dedicated progress method if available
        if hasattr(self.context, 'progress') and callable(self.context.progress):
            try:
                self.context.progress(
                    self.current, self.total, self.description)
                return
            except Exception:
                pass
        # Fallback to a generic log method
        if hasattr(self.context, 'log') and callable(self.context.log):
            try:
                self.context.log(
                    f'{self.description}: {self.current}/{self.total}')
            except Exception:
                pass

    def update(self, step: int = 1) -> None:
        '''
        Update progress by a number of steps.
        Args:
            step: Number of steps to add to progress
        '''
        if step < 0:
            raise ValueError("step must be non‑negative")
        self.current += step
        if self.current > self.total:
            self.current = self.total
        self._report()

    def set_progress(self, current: int) -> None:
        '''
        Set progress to a specific value.
        Args:
            current: Current progress value
        '''
        if current < 0:
            current = 0
        if current > self.total:
            current = self.total
        self.current = current
        self._report()
