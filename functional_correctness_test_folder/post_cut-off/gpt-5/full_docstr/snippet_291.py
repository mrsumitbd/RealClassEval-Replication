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
        if not isinstance(total, int):
            raise TypeError("total must be an int")
        if total < 0:
            raise ValueError("total must be >= 0")
        self.context = context
        self.total = total
        self.description = description
        self.current = 0
        self._done = total == 0
        from threading import Lock
        self._lock = Lock()

    def update(self, step: int = 1) -> None:
        '''
        Update progress by a number of steps.
        Args:
            step: Number of steps to add to progress
        '''
        if not isinstance(step, int):
            raise TypeError("step must be an int")
        if step < 0:
            raise ValueError("step must be >= 0")
        with self._lock:
            new_val = self.current + step
            if new_val > self.total:
                new_val = self.total
            self.current = new_val
            self._done = self.current >= self.total

    def set_progress(self, current: int) -> None:
        '''
        Set progress to a specific value.
        Args:
            current: Current progress value
        '''
        if not isinstance(current, int):
            raise TypeError("current must be an int")
        if current < 0 or current > self.total:
            raise ValueError("current must be within [0, total]")
        with self._lock:
            self.current = current
            self._done = self.current >= self.total
