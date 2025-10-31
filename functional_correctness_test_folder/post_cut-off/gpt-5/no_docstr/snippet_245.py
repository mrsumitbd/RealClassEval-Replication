from typing import Callable, Dict
import threading


class CallableRegistry:
    _registry: Dict[str, Callable] = {}
    _lock = threading.RLock()

    @classmethod
    def register(cls, name: str, callable_obj: Callable) -> None:
        if not isinstance(name, str) or not name:
            raise ValueError("name must be a non-empty string")
        if not callable(callable_obj):
            raise TypeError("callable_obj must be callable")
        with cls._lock:
            cls._registry[name] = callable_obj

    @classmethod
    def get(cls, name: str) -> Callable:
        with cls._lock:
            try:
                return cls._registry[name]
            except KeyError:
                raise KeyError(
                    f"No callable registered under name: {name}") from None

    @classmethod
    def contains(cls, name: str) -> bool:
        with cls._lock:
            return name in cls._registry
