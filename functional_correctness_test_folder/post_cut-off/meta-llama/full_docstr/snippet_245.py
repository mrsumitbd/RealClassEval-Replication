
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
        if not callable(callable_obj):
            raise TypeError("callable_obj is not callable")
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
        try:
            return cls._registry[name]
        except KeyError:
            raise KeyError(f"No callable registered with name '{name}'")

    @classmethod
    def contains(cls, name: str) -> bool:
        '''Check if a callable with the given name is registered.
        Args:
            name: Name to check
        Returns:
            True if registered, False otherwise
        '''
        return name in cls._registry


# Example usage:
def example_function():
    print("Hello, world!")


def main():
    CallableRegistry.register("example", example_function)
    print(CallableRegistry.contains("example"))  # True
    print(CallableRegistry.contains("nonexistent"))  # False
    retrieved_callable = CallableRegistry.get("example")
    retrieved_callable()  # Prints: Hello, world!
    try:
        CallableRegistry.get("nonexistent")
    except KeyError as e:
        print(e)  # Prints: No callable registered with name 'nonexistent'


if __name__ == "__main__":
    main()
