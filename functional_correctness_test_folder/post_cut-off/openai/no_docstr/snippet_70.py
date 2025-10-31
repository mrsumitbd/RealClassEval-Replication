
from typing import Any


class PrintingCallbackHandler:
    def __init__(self) -> None:
        pass

    def __call__(self, **kwargs: Any) -> None:
        print(kwargs)
