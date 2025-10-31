
from typing import Any, Callable


class ClassWithInitArgs:

    def __init__(self, cls: Callable, *args, **kwargs) -> None:
        self.cls = cls
        self.args = args
        self.kwargs = kwargs

    def __call__(self) -> Any:
        return self.cls(*self.args, **self.kwargs)
