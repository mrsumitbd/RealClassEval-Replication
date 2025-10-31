from typing import Any
import sys


class PrintingCallbackHandler:

    def __init__(self) -> None:
        '''Initialize handler.'''
        self._stream = sys.stdout

    def __call__(self, **kwargs: Any) -> None:
        parts = []
        for key in sorted(kwargs.keys()):
            try:
                val_repr = repr(kwargs[key])
            except Exception:
                val_repr = f"<unreprable {type(kwargs[key]).__name__}>"
            parts.append(f"{key}={val_repr}")
        print("Callback: " + ", ".join(parts), file=self._stream)
