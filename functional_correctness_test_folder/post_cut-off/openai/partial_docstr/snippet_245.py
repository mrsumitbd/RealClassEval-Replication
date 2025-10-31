
from __future__ import annotations
from typing import Callable, Dict


class CallableRegistry:
    """Registry for callable objects.

    This class serves as a central registry for callable objects (functions, methods)
    that can be referenced by name in serialized formats.
    """

    _registry: Dict[str, Callable] = {}

    @classmethod
    def register(cls, name: str, callable_obj: Callable) -> None:
        """Register a callable under a given name.

        Args:
            name: The name to register the callable under.
            callable_obj: The callable object to register.

        Raises:
            ValueError: If the name is already registered.
        """
        if name in cls._registry:
            raise ValueError(f"Callable name '{name}' is already registered.")
        cls._registry[name] = callable_obj

    @classmethod
    def get(cls, name: str) -> Callable:
        """Get a callable object by name.

        Args:
            name: Name of the callable to retrieve

        Returns:
            The registered callable

        Raises:
            KeyError: If no callable with the given name is registered
        """
        try:
            return cls._registry[name]
        except KeyError as exc:
            raise KeyError(
                f"No callable registered under name '{name}'.") from exc

    @classmethod
    def contains(cls, name: str) -> bool:
        """Check if a callable with the given name is registered.

        Args:
            name: Name to check

        Returns:
            True if registered, False otherwise
        """
        return name in cls._registry
