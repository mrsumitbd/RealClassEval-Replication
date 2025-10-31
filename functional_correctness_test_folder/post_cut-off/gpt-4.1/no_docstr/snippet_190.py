
from typing import Any


class ClassWithInitArgs:

    def __init__(self, cls, *args, **kwargs) -> None:
        self._cls = cls
        self._args = args
        self._kwargs = kwargs

    def __call__(self) -> Any:
        return self._cls(*self._args, **self._kwargs)
