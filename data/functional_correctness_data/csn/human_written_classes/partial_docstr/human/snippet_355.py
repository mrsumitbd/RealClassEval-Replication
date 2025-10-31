from functools import _c3_mro
from typing import Any, Callable, Dict, Optional
from collections import OrderedDict

class singledispatchbymatchfunction:
    """
    Inspired by @singledispatch, this is a variant that works using a matcher function
    instead of relying on the type of the first argument.
    The register method can be used to register a new matcher, which is passed as the first argument:
    """

    def __init__(self, default: Callable):
        self.registry: Dict[Callable, Callable] = OrderedDict()
        self.default = default

    def __call__(self, *args, **kwargs):
        matched_arg = args[0]
        try:
            mro = _c3_mro(matched_arg)
        except Exception:
            mro = [matched_arg]
        for cls in mro:
            for matcher_function, final_method in self.registry.items():
                if matcher_function(cls):
                    return final_method(*args, **kwargs)
        return self.default(*args, **kwargs)

    def register(self, matcher_function: Callable[[Any], bool], func=None):
        if func is None:
            return lambda f: self.register(matcher_function, f)
        self.registry[matcher_function] = func
        return func