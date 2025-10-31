from typing import Any, Callable, FrozenSet, Iterable, List, Optional, Tuple
import inspect
import sys


class CompositeCallbackHandler:
    '''Class-based callback handler that combines multiple callback handlers.
    This handler allows multiple callback handlers to be invoked for the same events,
    enabling different processing or output formats for the same stream data.
    '''

    def __init__(self, *handlers: Callable) -> None:
        '''Initialize handler.'''
        normalized: List[Callable] = []

        # Support passing a single iterable of handlers
        if len(handlers) == 1 and not callable(handlers[0]) and isinstance(
            handlers[0], Iterable
        ) and not isinstance(handlers[0], (str, bytes, bytearray)):
            handlers = tuple(handlers[0])  # type: ignore[assignment]

        for h in handlers:
            if h is None:
                continue
            if isinstance(h, CompositeCallbackHandler):
                normalized.extend(h._handlers)
            else:
                if not callable(h):
                    raise TypeError(f'Handler {h!r} is not callable')
                normalized.append(h)

        self._handlers: Tuple[Callable, ...] = tuple(normalized)
        self._specs: Tuple[Tuple[Callable, Optional[bool], FrozenSet[str]], ...] = tuple(
            self._introspect(h) for h in self._handlers
        )

    def __call__(self, **kwargs: Any) -> None:
        '''Invoke all handlers in the chain.'''
        first_exc_info = None

        for handler, accepts_var_kw, accepted_names in self._specs:
            try:
                if accepts_var_kw is None:
                    # Unknown signature: try with kwargs, fallback to no-args on TypeError
                    try:
                        handler(**kwargs)
                    except TypeError:
                        handler()
                else:
                    if accepts_var_kw:
                        handler(**kwargs)
                    else:
                        filtered = {k: v for k, v in kwargs.items()
                                    if k in accepted_names}
                        handler(**filtered)
            except Exception:
                if first_exc_info is None:
                    first_exc_info = sys.exc_info()
                continue

        if first_exc_info is not None:
            _, exc, tb = first_exc_info
            raise exc.with_traceback(tb)

    @staticmethod
    def _introspect(handler: Callable) -> Tuple[Callable, Optional[bool], FrozenSet[str]]:
        try:
            sig = inspect.signature(handler)
        except (TypeError, ValueError):
            # Unable to introspect signature; mark as unknown
            return handler, None, frozenset()

        accepts_var_kw = any(
            p.kind is inspect.Parameter.VAR_KEYWORD for p in sig.parameters.values())
        accepted_names = frozenset(
            p.name
            for p in sig.parameters.values()
            if p.kind in (inspect.Parameter.KEYWORD_ONLY, inspect.Parameter.POSITIONAL_OR_KEYWORD)
        )
        return handler, accepts_var_kw, accepted_names
