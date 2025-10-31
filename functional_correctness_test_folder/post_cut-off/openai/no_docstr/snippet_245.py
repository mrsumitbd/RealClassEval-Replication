
from typing import Callable, Dict


class CallableRegistry:
    _registry: Dict[str, Callable] = {}

    @classmethod
    def register(cls, name: str, callable_obj: Callable) -> None:
        """
        Register a callable under the given name. If the name already exists,
        the existing callable will be overwritten.
        """
        if not isinstance(name, str):
            raise TypeError("name must be a string")
        if not callable(callable_obj):
            raise TypeError("callable_obj must be callable")
        cls._registry[name] = callable_obj

    @classmethod
    def get(cls, name: str) -> Callable:
        """
        Retrieve the callable registered under the given name.
        Raises KeyError if the name is not found.
        """
        try:
            return cls._registry[name]
        except KeyError:
            raise KeyError(
                f"No callable registered under name '{name}'") from None

    @classmethod
    def contains(cls, name: str) -> bool:
        """
        Return True if a callable is registered under the given name, False otherwise.
        """
        return name in cls._registry
