from typing import Any, Callable, Tuple


class CompositeCallbackHandler:
    """Class-based callback handler that combines multiple callback handlers.
    This handler allows multiple callback handlers to be invoked for the same events,
    enabling different processing or output formats for the same stream data.
    """

    def __init__(self, *handlers: Callable) -> None:
        """Initialize handler."""
        flat_handlers = []
        for h in handlers:
            if isinstance(h, CompositeCallbackHandler):
                flat_handlers.extend(h._handlers)
            elif callable(h):
                flat_handlers.append(h)
            else:
                raise TypeError(f'Handler {h!r} is not callable')
        self._handlers: Tuple[Callable, ...] = tuple(flat_handlers)

    def __call__(self, **kwargs: Any) -> None:
        """Invoke all handlers in the chain."""
        for handler in self._handlers:
            handler(**kwargs)
