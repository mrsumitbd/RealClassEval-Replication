
from typing import Any


class PrintingCallbackHandler:
    def __init__(self) -> None:
        '''Initialize handler.'''
        # No special initialization required
        pass

    def __call__(self, **kwargs: Any) -> None:
        """Print all keyword arguments passed to the handler."""
        if not kwargs:
            print("PrintingCallbackHandler called with no arguments.")
            return
        for key, value in kwargs.items():
            print(f"{key} = {value!r}")
