
class ProgressScope:

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

    def update(self, step: int = 1) -> None:
        self.current += step
        if hasattr(self.context, 'update_progress'):
            self.context.update_progress(
                self.current, self.total, self.description)

    def set_progress(self, current: int) -> None:
        self.current = current
        if hasattr(self.context, 'update_progress'):
            self.context.update_progress(
                self.current, self.total, self.description)
