
from typing import Callable, Any


class CompositeCallbackHandler:

    def __init__(self, *handlers: Callable) -> None:
        self.handlers = handlers

    def __call__(self, **kwargs: Any) -> None:
        for handler in self.handlers:
            handler(**kwargs)
