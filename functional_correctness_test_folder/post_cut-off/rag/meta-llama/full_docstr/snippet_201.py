
from dataclasses import dataclass, fields


@dataclass
class OverridableConfig:
    """A class that provides an interface to switch between its field values depending on an override key."""

    def __post_init__(self) -> None:
        """Initialize the override key to 'default'."""
        self._override_key = 'default'
        self._override_registry = {}

    def set_override(self, key: str, reset_to_defaults: bool = True) -> None:
        """Set the overridden values for the config based on the override registry.

        Args:
            key: The key to use for the override.
            reset_to_defaults: If True, reset the values to their defaults if no override is found. This is useful for
                when you switch from different non-default overrides to other non-default overrides.
        """
        self._override_key = key
        for field in fields(self):
            override_value = self._override_registry.get(
                key, {}).get(field.name)
            if override_value is not None:
                setattr(self, field.name, override_value)
            elif reset_to_defaults:
                setattr(self, field.name, field.default)
