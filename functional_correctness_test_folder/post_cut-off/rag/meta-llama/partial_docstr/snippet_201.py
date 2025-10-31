
from dataclasses import dataclass, fields, is_dataclass
from typing import Any


@dataclass
class OverridableConfig:
    """A class that provides an interface to switch between its field values depending on an override key."""

    def __post_init__(self) -> None:
        """Initialize the override key to 'default'."""
        self._override_key = 'default'
        self._override_registry: dict[str, dict[str, Any]] = {'default': {}}

    def set_override(self, key: str, reset_to_defaults: bool = True) -> None:
        """Set the overridden values for the config based on the override registry.

        Args:
            key: The key to use for the override.
            reset_to_defaults: If True, reset the values to their defaults if no override is found. This is useful for
                when you switch from different non-default overrides to other non-default overrides.
        """
        if not hasattr(self, '_override_registry'):
            raise AttributeError(
                'Override registry not found. Did you forget to call super().__post_init__()?')

        if key not in self._override_registry:
            if reset_to_defaults:
                for field in fields(self):
                    setattr(self, field.name, field.default)
            return

        override_values = self._override_registry[key]
        for field in fields(self):
            if field.name in override_values:
                setattr(self, field.name, override_values[field.name])
            elif reset_to_defaults:
                setattr(self, field.name, field.default)

        self._override_key = key

    @classmethod
    def register_override(cls, key: str, **kwargs) -> None:
        """Register an override with the given key and values.

        Args:
            key: The key to use for the override.
            **kwargs: The values to override.
        """
        if not hasattr(cls, '_override_registry'):
            cls._override_registry = {'default': {}}

        if key in cls._override_registry:
            raise ValueError(f'Override key {key} already exists')

        cls._override_registry[key] = kwargs

    def __init_subclass__(cls) -> None:
        """Ensure that the subclass is a dataclass."""
        if not is_dataclass(cls):
            raise TypeError('OverridableConfig subclasses must be dataclasses')
