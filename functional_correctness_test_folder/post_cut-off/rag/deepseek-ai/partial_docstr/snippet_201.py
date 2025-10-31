
from dataclasses import dataclass


@dataclass
class OverridableConfig:
    """A class that provides an interface to switch between its field values depending on an override key."""

    def __post_init__(self) -> None:
        """Initialize the override key to 'default'."""
        self._override_key = 'default'

    def set_override(self, key: str, reset_to_defaults: bool = True) -> None:
        """Set the overridden values for the config based on the override registry.

        Args:
            key: The key to use for the override.
            reset_to_defaults: If True, reset the values to their defaults if no override is found. This is useful for
                when you switch from different non-default overrides to other non-default overrides.
        """
        self._override_key = key
        if reset_to_defaults and key not in self._override_registry:
            for field_name, field_value in self.__dataclass_fields__.items():
                if hasattr(field_value, 'default'):
                    setattr(self, field_name, field_value.default)
