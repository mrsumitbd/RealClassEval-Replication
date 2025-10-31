
from typing import Callable


class CallableRegistry:
    _registry = {}

    @classmethod
    def register(cls, name: str, callable_obj: Callable) -> None:
        cls._registry[name] = callable_obj

    @classmethod
    def get(cls, name: str) -> Callable:
        if name not in cls._registry:
            raise KeyError(f"No callable registered under name '{name}'")
        return cls._registry[name]

    @classmethod
    def contains(cls, name: str) -> bool:
        return name in cls._registry
