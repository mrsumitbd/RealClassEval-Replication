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
        self.total = total
        self.description = description
        self.current = 0

        # Try to initialise a progress bar if the context provides one
        if hasattr(context, 'progress'):
            try:
                progress = context.progress
                # If the progress object looks like tqdm, set total and description
                if hasattr(progress, 'total'):
                    progress.total = total
                if hasattr(progress, 'set_description'):
                    progress.set_description(description)
                if hasattr(progress, 'update'):
                    progress.update(0)
            except Exception:
                # Silently ignore any failure to initialise the progress bar
                pass

    def update(self, step: int = 1) -> None:
        '''
        Update progress by a number of steps.
        Args:
            step: Number of steps to add to progress
        '''
        self.current += step
        if self.current > self.total:
            self.current = self.total

        # Update the progress bar if available
        if hasattr(self.context, 'progress'):
            try:
                progress = self.context.progress
                if hasattr(progress, 'update'):
                    # If the progress object expects a delta, use step
                    progress.update(step)
                else:
                    # Fallback: try to set the progress to the current value
                    progress.current = self.current
            except Exception:
                pass

    def set_progress(self, current: int) -> None:
        '''
        Set progress to a specific value.
        Args:
            current: Current progress value
        '''
        self.current = current
        if self.current > self.total:
            self.current = self.total

        # Update the progress bar if available
        if hasattr(self.context, 'progress'):
            try:
                progress = self.context.progress
                if hasattr(progress, 'update'):
                    # Compute the delta needed to reach the desired current value
                    delta = self.current - getattr(progress, 'n', 0)
                    if delta > 0:
                        progress.update(delta)
                else:
                    progress.current = self.current
            except Exception:
                pass
