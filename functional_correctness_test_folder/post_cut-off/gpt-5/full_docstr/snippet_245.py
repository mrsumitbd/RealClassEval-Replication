from typing import Callable, Dict
import threading


class CallableRegistry:
    '''Registry for callable objects.
    This class serves as a central registry for callable objects (functions, methods)
    that can be referenced by name in serialized formats.
    This is a placeholder implementation that will be fully implemented in task US007-T004.
    '''

    _registry: Dict[str, Callable] = {}
    _lock = threading.RLock()

    @classmethod
    def register(cls, name: str, callable_obj: Callable) -> None:
        '''Register a callable object with the given name.
        Args:
            name: Unique name for the callable
            callable_obj: Function or method to register
        '''
        if not isinstance(name, str):
            raise TypeError("name must be a string")
        if not name:
            raise ValueError("name must be a non-empty string")
        if not callable(callable_obj):
            raise TypeError("callable_obj must be callable")

        with cls._lock:
            existing = cls._registry.get(name)
            if existing is not None and existing is not callable_obj:
                raise ValueError(
                    f"Callable name '{name}' is already registered")
            cls._registry[name] = callable_obj

    @classmethod
    def get(cls, name: str) -> Callable:
        '''Get a callable object by name.
        Args:
            name: Name of the callable to retrieve
        Returns:
            The registered callable
        Raises:
            KeyError: If no callable with the given name is registered
        '''
        with cls._lock:
            try:
                return cls._registry[name]
            except KeyError as e:
                raise KeyError(
                    f"No callable registered under name '{name}'") from e

    @classmethod
    def contains(cls, name: str) -> bool:
        '''Check if a callable with the given name is registered.
        Args:
            name: Name to check
        Returns:
            True if registered, False otherwise
        '''
        with cls._lock:
            return name in cls._registry
