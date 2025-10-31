from easyswitch.exceptions import InvalidProviderError
from typing import Any, ClassVar, Dict, List, Optional, Type, Union

class AdaptersRegistry:
    """
    Registry for all payment adapters.
    This class is used to register and retrieve adapters based on their provider.
    """
    _registry: ClassVar[Dict[str, Type['BaseAdapter']]] = {}

    @classmethod
    def register(cls, name: Optional[str]=None) -> None:
        """Register a new Adapter class."""

        def wrapper(adapter: Type['BaseAdapter']):
            """Wrapper"""
            nonlocal name
            name = name or adapter.provider_name()
            name = name.upper()
            if not name in cls._registry.keys():
                cls._registry[name] = adapter
            return adapter
        return wrapper

    @classmethod
    def get(cls, name: str) -> Type['BaseAdapter']:
        """Get an Adapter class by its name."""
        if name not in cls._registry:
            raise InvalidProviderError(f"Invalid Adapter name: '{name}' not found.")
        return cls._registry[name]

    @classmethod
    def all(cls) -> List[Type['BaseAdapter']]:
        """Get all registered Adapters classes."""
        return list(cls._registry.values())

    @classmethod
    def clear(cls) -> None:
        """Clear the registry."""
        cls._registry.clear()

    @classmethod
    def list(cls) -> List[str]:
        """List all registered Adapters names."""
        return list(cls._registry.keys())