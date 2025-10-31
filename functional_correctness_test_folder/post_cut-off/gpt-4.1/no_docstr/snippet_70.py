
from typing import Any


class PrintingCallbackHandler:

    def __init__(self) -> None:
        pass

    def __call__(self, **kwargs: Any) -> None:
        for key, value in kwargs.items():
            print(f"{key}: {value}")
