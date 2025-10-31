from typing import Any, List, Dict


class PrintingCallbackHandler:

    def __init__(self) -> None:
        self.history: List[Dict[str, Any]] = []

    def __call__(self, **kwargs: Any) -> None:
        self.history.append(dict(kwargs))
        if not kwargs:
            print("PrintingCallbackHandler: (no arguments)")
            return
        parts = [f"{k}={repr(kwargs[k])}" for k in sorted(kwargs.keys())]
        print("PrintingCallbackHandler: " + ", ".join(parts))
