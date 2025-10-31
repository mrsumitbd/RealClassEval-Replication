
from dataclasses import dataclass, field, fields
from typing import Any, Dict, ClassVar


@dataclass
class OverridableConfig:
    """A class that provides an interface to switch between its field values
    depending on an override key.
    """

    # Class‑level registry of overrides: key -> dict of field_name -> value
    _override_registry: ClassVar[Dict[str, Dict[str, Any]]] = {}

    # Instance attributes
    _override_key: str = field(init=False, repr=False, default="default")
    _defaults: Dict[str, Any] = field(
        init=False, repr=False, default_factory=dict)

    def __post_init__(self) -> None:
        """Initialize the override key to 'default' and store the default values."""
        # Store the default values of all fields
        self._defaults = {f.name: getattr(self, f.name)
                          for f in fields(self) if f.init}
        # Set the current override key
        self._override_key = "default"

    def set_override(self, key: str, reset_to_defaults: bool = True) -> None:
        """
        Set the overridden values for the config based on the override registry.

        Args:
            key: The key to use for the override.
            reset_to_defaults: If True, reset the values to their defaults if no override is found.
                This is useful when you switch from different non‑default overrides to other non‑default overrides.
        """
        # Update the current override key
        self._override_key = key

        # Retrieve the override mapping for the key, if any
        override_map = self._override_registry.get(key)

        if override_map is not None:
            # Apply each override value
            for field_name, value in override_map.items():
                if hasattr(self, field_name):
                    setattr(self, field_name, value)
        else:
            # No override found
            if reset_to_defaults:
                # Reset to the stored defaults
                for field_name, default_value in self._defaults.items():
                    setattr(self, field_name, default_value)

    @classmethod
    def register_override(cls, key: str, overrides: Dict[str, Any]) -> None:
        """
        Register a set of overrides for a given key.

        Args:
            key: The override key.
            overrides: A mapping of field names to override values.
        """
        cls._override_registry[key] = overrides.copy()
