
from typing import Any, Callable, Iterable, Tuple


class CompositeCallbackHandler:
    '''Class-based callback handler that combines multiple callback handlers.
    This handler allows multiple callback handlers to be invoked for the same events,
    enabling different processing or output formats for the same stream data.
    '''

    def __init__(self, *handlers: Callable) -> None:
        self.handlers: Tuple[Callable, ...] = handlers

    def __call__(self, **kwargs: Any) -> None:
        '''Invoke all handlers in the chain.'''
        for handler in self.handlers:
            handler(**kwargs)
