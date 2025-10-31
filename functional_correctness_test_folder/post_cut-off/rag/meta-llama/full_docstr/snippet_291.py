
class ProgressScope:
    """Scope for tracking progress of an operation."""

    def __init__(self, context: 'MCPContext', total: int, description: str):
        """
        Initialize a progress scope.

        Args:
            context: The parent MCPContext
            total: Total number of steps
            description: Description of the operation
        """
        self.context = context
        self.total = total
        self.description = description
        self.current = 0
        self.context._progress_start(description, total)

    def update(self, step: int = 1) -> None:
        """
        Update progress by a number of steps.

        Args:
            step: Number of steps to add to progress
        """
        self.set_progress(self.current + step)

    def set_progress(self, current: int) -> None:
        """
        Set progress to a specific value.

        Args:
            current: Current progress value
        """
        if current > self.total:
            current = self.total
        if current < 0:
            current = 0
        self.current = current
        self.context._progress_update(current)
        if current == self.total:
            self.context._progress_end()
