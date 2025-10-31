
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
        if progress and hasattr(progress, 'start'):
            try:
                progress.start(self.total, self.description)
            except Exception:
                # Silently ignore any progress bar initialisation errors
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
        progress = getattr(self.context, 'progress', None)
        if progress and hasattr(progress, 'update'):
            try:
                progress.update(self.current)
            except Exception:
                pass

    def set_progress(self, current: int) -> None:
        '''
        Set progress to a specific value.
        Args:
            current: Current progress value
        '''
        self.current = max(0, int(current))
        if self.current > self.total:
            self.current = self.total
        progress = getattr(self.context, 'progress', None)
        if progress and hasattr(progress, 'update'):
            try:
                progress.update(self.current)
            except Exception:
                pass
