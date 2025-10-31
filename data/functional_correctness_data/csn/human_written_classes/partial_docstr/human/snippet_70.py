import typing as t

class AttemptManager:
    """Manage attempt context."""

    def __init__(self, retry_state: 'RetryCallState'):
        self.retry_state = retry_state

    def __enter__(self) -> None:
        pass

    def __exit__(self, exc_type: t.Optional[t.Type[BaseException]], exc_value: t.Optional[BaseException], traceback: t.Optional['types.TracebackType']) -> t.Optional[bool]:
        if exc_type is not None and exc_value is not None:
            self.retry_state.set_exception((exc_type, exc_value, traceback))
            return True
        else:
            self.retry_state.set_result(None)
            return None