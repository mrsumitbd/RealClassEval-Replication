
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
        if hasattr(self.context, 'on_progress_start'):
            self.context.on_progress_start(self.description, self.total)

    def update(self, step: int = 1) -> None:
        self.current += step
        if self.current > self.total:
            self.current = self.total
        if hasattr(self.context, 'on_progress_update'):
            self.context.on_progress_update(
                self.current, self.total, self.description)

    def set_progress(self, current: int) -> None:
        self.current = max(0, min(current, self.total))
        if hasattr(self.context, 'on_progress_update'):
            self.context.on_progress_update(
                self.current, self.total, self.description)
