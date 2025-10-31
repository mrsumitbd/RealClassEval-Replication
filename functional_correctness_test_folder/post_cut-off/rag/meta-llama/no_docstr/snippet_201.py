
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
        if reset_to_defaults:
            for field in fields(self):
                setattr(self, field.name, field.default)

        if key in self._override_registry:
            overrides = self._override_registry[key]
            for field_name, value in overrides.items():
                setattr(self, field_name, value)

    def register_override(self, key: str, overrides: dict) -> None:
        """Register an override.

        Args:
            key: The key to use for the override.
            overrides: A dictionary of field names to override values.
        """
        self._override_registry[key] = overrides
