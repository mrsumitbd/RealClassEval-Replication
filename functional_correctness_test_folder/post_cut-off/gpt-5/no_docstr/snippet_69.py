from typing import Any, Callable, Tuple


class CompositeCallbackHandler:
    def __init__(self, *handlers: Callable) -> None:
        flat: Tuple[Callable, ...]
        if len(handlers) == 1 and isinstance(handlers[0], (list, tuple, set)):
            flat = tuple(handlers[0])  # type: ignore[arg-type]
        else:
            flat = tuple(handlers)
        for h in flat:
            if not callable(h):
                raise TypeError(f"Handler {h!r} is not callable")
        self._handlers: Tuple[Callable, ...] = flat

    def __call__(self, **kwargs: Any) -> None:
        for handler in self._handlers:
            handler(**kwargs)
