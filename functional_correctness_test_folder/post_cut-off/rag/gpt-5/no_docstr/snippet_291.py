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
        if total < 0:
            raise ValueError('total must be >= 0')
        self.context = context
        self.total = int(total)
        self.description = description
        self.current = 0
        self._lock = __import__('threading').Lock()
        self._emit_progress()

    def update(self, step: int = 1) -> None:
        '''
        Update progress by a number of steps.
        Args:
            step: Number of steps to add to progress
        '''
        with self._lock:
            self.current = max(0, min(self.total, self.current + int(step)))
            self._emit_progress()

    def set_progress(self, current: int) -> None:
        '''
        Set progress to a specific value.
        Args:
            current: Current progress value
        '''
        with self._lock:
            self.current = max(0, min(self.total, int(current)))
            self._emit_progress()

    def _emit_progress(self) -> None:
        cb_names = ('on_progress', 'update_progress',
                    'report_progress', 'progress', 'progress_callback')
        for name in cb_names:
            cb = getattr(self.context, name, None)
            if callable(cb):
                try:
                    cb(total=self.total, current=self.current,
                       description=self.description)
                except TypeError:
                    try:
                        cb(self.total, self.current, self.description)
                    except Exception:
                        pass
                break
