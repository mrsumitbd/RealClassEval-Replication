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
        from threading import Lock

        if total < 0:
            raise ValueError('total must be >= 0')

        self.context = context
        self.total = int(total)
        self.description = description
        self.current = 0
        self._lock = Lock()

        # Emit initial progress
        self._emit_progress()

    def update(self, step: int = 1) -> None:
        '''
        Update progress by a number of steps.
        Args:
            step: Number of steps to add to progress
        '''
        if step < 0:
            raise ValueError('step must be >= 0')
        with self._lock:
            self.current = min(self.total, self.current + int(step))
            self._emit_progress()

    def set_progress(self, current: int) -> None:
        '''
        Set progress to a specific value.
        Args:
            current: Current progress value
        '''
        if current < 0:
            raise ValueError('current must be >= 0')
        with self._lock:
            self.current = min(self.total, int(current))
            self._emit_progress()

    def _emit_progress(self) -> None:
        percent = (self.current / self.total) if self.total > 0 else 0.0
        payload = {
            'description': self.description,
            'current': self.current,
            'total': self.total,
            'percent': percent,
            'done': self.current >= self.total,
        }

        # Try common progress notification hooks on the context
        for name in (
            'emit_progress',
            'report_progress',
            'notify_progress',
            'on_progress',
            'update_progress',
            'progress_callback',
            'progress',
        ):
            fn = getattr(self.context, name, None)
            if callable(fn):
                try:
                    try:
                        fn(**payload)
                    except TypeError:
                        fn(payload)
                except Exception:
                    # Silently ignore notification errors to avoid interrupting progress
                    pass
                break
