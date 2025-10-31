from typing import Dict, Callable, Any, Optional, List

class tool:
    """
    A tool that can be used to execute a function.
    """

    def __init__(self, func: Callable):
        self.func = func
        self.name = func.__name__

    def __get__(self, instance, owner):
        if instance is None:
            return self
        return lambda *args, **kwargs: self.func(instance, *args, **kwargs)