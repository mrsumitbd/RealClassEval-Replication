
from typing import Any, Callable, Iterable, List


class CompositeCallbackHandler:
    """
    A simple composite callback handler that forwards calls to multiple
    underlying handlers.

    Parameters
    ----------
    *handlers : Callable
        Any number of callables that will be invoked when the composite
        handler is called. Each callable should accept keyword arguments.
    """

    def __init__(self, *handlers: Callable) -> None:
        # Store handlers as a list for easy iteration
        self._handlers: List[Callable] = list(handlers)

    def __call__(self, **kwargs: Any) -> None:
        """
        Invoke all stored handlers with the provided keyword arguments.

        Parameters
        ----------
        **kwargs : Any
            Keyword arguments to forward to each handler.
        """
        for handler in self._handlers:
            handler(**kwargs)
