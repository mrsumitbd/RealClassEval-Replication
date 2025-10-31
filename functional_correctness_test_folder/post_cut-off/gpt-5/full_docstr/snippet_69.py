from typing import Any, Callable, Iterable, Tuple
import inspect


class CompositeCallbackHandler:
    '''Class-based callback handler that combines multiple callback handlers.
    This handler allows multiple callback handlers to be invoked for the same events,
    enabling different processing or output formats for the same stream data.
    '''

    def __init__(self, *handlers: Callable) -> None:
        '''Initialize handler.'''
        # Allow passing an iterable of handlers as a single argument
        if len(handlers) == 1 and not callable(handlers[0]) and isinstance(handlers[0], Iterable):
            handlers = tuple(handlers[0])  # type: ignore[assignment]

        if not handlers:
            self._handlers: Tuple[Callable, ...] = ()
            return

        for h in handlers:
            if not callable(h):
                raise TypeError(f"Handler {h!r} is not callable")
        self._handlers = tuple(handlers)

    def __call__(self, **kwargs: Any) -> None:
        '''Invoke all handlers in the chain.'''
        for handler in self._handlers:
            self._invoke_handler(handler, kwargs)

    @staticmethod
    def _invoke_handler(handler: Callable, kwargs: dict) -> None:
        sig = None
        try:
            sig = inspect.signature(handler)
        except (TypeError, ValueError):
            # Fallback: if we can't inspect, try with all kwargs
            handler(**kwargs)  # type: ignore[misc]
            return

        params = sig.parameters
        accepts_varkw = any(p.kind == p.VAR_KEYWORD for p in params.values())
        if accepts_varkw:
            handler(**kwargs)  # type: ignore[misc]
            return

        accepted_keys = {name for name, p in params.items()
                         if p.kind in (p.POSITIONAL_OR_KEYWORD, p.KEYWORD_ONLY)}
        filtered = {k: v for k, v in kwargs.items() if k in accepted_keys}
        handler(**filtered)  # type: ignore[misc]
