
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
        self.context.progress_start(total, description)

    def update(self, step: int = 1) -> None:
        '''
        Update progress by a number of steps.
        Args:
            step: Number of steps to add to progress
        '''
        self.current += step
        self.context.progress_update(self.current)

    def set_progress(self, current: int) -> None:
        '''
        Set progress to a specific value.
        Args:
            current: Current progress value
        '''
        self.current = current
        self.context.progress_update(self.current)
