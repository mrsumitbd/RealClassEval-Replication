from typing import Callable


class CallableRegistry:
    '''Registry for callable objects.
    This class serves as a central registry for callable objects (functions, methods)
    that can be referenced by name in serialized formats.
    This is a placeholder implementation that will be fully implemented in task US007-T004.
    '''
    _registry = {}

    @classmethod
    def register(cls, name: str, callable_obj: Callable) -> None:
        '''Register a callable object with the given name.
        Args:
            name: Unique name for the callable
            callable_obj: Function or method to register
        '''
        if not isinstance(name, str):
            raise TypeError('name must be a string')
        key = name.strip()
        if not key:
            raise ValueError('name must be a non-empty string')
        if not callable(callable_obj):
            raise TypeError('callable_obj must be callable')
        if key in cls._registry:
            raise KeyError(f'callable already registered for name: {name}')
        cls._registry[key] = callable_obj

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
        if not isinstance(name, str):
            raise TypeError('name must be a string')
        key = name.strip()
        if key not in cls._registry:
            raise KeyError(f'no callable registered for name: {name}')
        return cls._registry[key]

    @classmethod
    def contains(cls, name: str) -> bool:
        '''Check if a callable with the given name is registered.
        Args:
            name: Name to check
        Returns:
            True if registered, False otherwise
        '''
        if not isinstance(name, str):
            return False
        key = name.strip()
        if not key:
            return False
        return key in cls._registry
