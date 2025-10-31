from typing import Any, Callable, Optional

class ClassWithInitArgs:
    """
    This class stores a class constructor and the args/kwargs to construct the class.
    It is used to instantiate the remote class.
    """

    def __init__(self, cls, *args, **kwargs) -> None:
        self.cls = cls
        self.args = args
        self.kwargs = kwargs

    def __call__(self) -> Any:
        return self.cls(*self.args, **self.kwargs)