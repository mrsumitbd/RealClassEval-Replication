
from dataclasses import dataclass, fields


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
        for field in fields(self):
            if hasattr(self, f"{field.name}_override"):
                override_values = getattr(self, f"{field.name}_override")
                if key in override_values:
                    setattr(self, field.name, override_values[key])
                elif reset_to_defaults:
                    default_value = getattr(
                        self, f"{field.name}_default", None)
                    if default_value is not None:
                        setattr(self, field.name, default_value)
