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
            raise ValueError('total must be non-negative')
        self.context = context
        self.total = int(total)
        self.description = description
        self.current = 0
        self._done_emitted = False
        # best-effort notify start
        self._notify_start()

    def update(self, step: int = 1) -> None:
        '''
        Update progress by a number of steps.
        Args:
            step: Number of steps to add to progress
        '''
        if not isinstance(step, int):
            raise TypeError('step must be an int')
        if step == 0:
            return
        new_val = self.current + step
        if new_val < 0:
            new_val = 0
        if self.total > 0 and new_val > self.total:
            new_val = self.total
        self.set_progress(new_val)

    def set_progress(self, current: int) -> None:
        '''
        Set progress to a specific value.
        Args:
            current: Current progress value
        '''
        if not isinstance(current, int):
            raise TypeError('current must be an int')
        if current < 0:
            current = 0
        if self.total > 0 and current > self.total:
            current = self.total
        self.current = current
        self._notify_update()
        if self.total > 0 and self.current >= self.total and not self._done_emitted:
            self._done_emitted = True
            self._notify_done()

    # Internal helpers

    def _try_call(self, method_name: str, *variants: tuple[tuple, dict]) -> bool:
        fn = getattr(self.context, method_name, None)
        if callable(fn):
            for args, kwargs in variants:
                try:
                    fn(*args, **kwargs)
                    return True
                except TypeError:
                    continue
        return False

    def _notify_start(self) -> None:
        payload = dict(total=self.total, description=self.description)
        # Try common method names/signatures; ignore if not available
        self._try_call(
            'progress_start',
            (tuple(), payload),
            ((self.total, self.description), {}),
            ((self.total,), {}),
        ) or self._try_call(
            'start_progress',
            (tuple(), payload),
            ((self.total, self.description), {}),
            ((self.total,), {}),
        ) or self._try_call(
            'on_progress_start',
            (tuple(), payload),
            ((self.total, self.description), {}),
            ((self.total,), {}),
        )

    def _notify_update(self) -> None:
        payload = dict(current=self.current, total=self.total,
                       description=self.description)
        self._try_call(
            'progress_update',
            (tuple(), payload),
            ((self.current, self.total, self.description), {}),
            ((self.current, self.total), {}),
            ((self.current,), {}),
        ) or self._try_call(
            'update_progress',
            (tuple(), payload),
            ((self.current, self.total, self.description), {}),
            ((self.current, self.total), {}),
            ((self.current,), {}),
        ) or self._try_call(
            'notify_progress',
            (tuple(), payload),
            ((self.current, self.total, self.description), {}),
            ((self.current, self.total), {}),
            ((self.current,), {}),
        ) or self._try_call(
            'report_progress',
            (tuple(), payload),
            ((self.current, self.total, self.description), {}),
            ((self.current, self.total), {}),
            ((self.current,), {}),
        )

    def _notify_done(self) -> None:
        payload = dict(total=self.total, description=self.description)
        self._try_call(
            'progress_done',
            (tuple(), payload),
            ((self.total, self.description), {}),
            ((self.total,), {}),
        ) or self._try_call(
            'finish_progress',
            (tuple(), payload),
            ((self.total, self.description), {}),
            ((self.total,), {}),
        ) or self._try_call(
            'end_progress',
            (tuple(), payload),
            ((self.total, self.description), {}),
            ((self.total,), {}),
        )
