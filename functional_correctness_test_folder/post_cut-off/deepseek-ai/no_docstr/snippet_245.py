
from typing import Callable, Dict


class CallableRegistry:
    _registry: Dict[str, Callable] = {}

    @classmethod
    def register(cls, name: str, callable_obj: Callable) -> None:
        cls._registry[name] = callable_obj

    @classmethod
    def get(cls, name: str) -> Callable:
        return cls._registry[name]

    @classmethod
    def contains(cls, name: str) -> bool:
        return name in cls._registry
