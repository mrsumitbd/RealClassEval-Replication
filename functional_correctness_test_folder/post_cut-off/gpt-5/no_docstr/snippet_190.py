from typing import Any, Callable


class ClassWithInitArgs:

    def __init__(self, cls: Callable[..., Any], *args: Any, **kwargs: Any) -> None:
        if not callable(cls):
            raise TypeError("cls must be callable")
        self._cls = cls
        self._args = args
        self._kwargs = kwargs

    def __call__(self) -> Any:
        return self._cls(*self._args, **self._kwargs)
