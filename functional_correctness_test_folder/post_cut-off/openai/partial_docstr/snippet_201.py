
from dataclasses import dataclass, fields
from typing import Any, Dict, ClassVar


@dataclass
class OverridableConfig:
    # Class‑level registry of overrides: key -> dict of attribute values
    _override_registry: ClassVar[Dict[str, Dict[str, Any]]] = {}

    # Instance attribute to keep track of the current override key
    override_key: str = "default"

    # Store the default values of all fields after initialization
    _defaults: Dict[str, Any] = None  # type: ignore

    def __post_init__(self) -> None:
        """Initialize the override key to 'default' and store defaults."""
        self.override_key = "default"
        # Capture the default values of all dataclass fields
        self._defaults = {f.name: getattr(self, f.name) for f in fields(self)}

    def set_override(self, key: str, reset_to_defaults: bool = True) -> None:
        """
        Set the overridden values for the config based on the override registry.

        Args:
            key: The key to use for the override.
            reset_to_defaults: If True, reset the values to their defaults if no override is found.
                This is useful when you switch from different non‑default overrides to other non‑default overrides.
        """
        # If the key is not in the registry and we should reset to defaults, do so
        if key not in self._override_registry:
            if reset_to_defaults:
                for field_name, default_value in self._defaults.items():
                    setattr(self, field_name, default_value)
            # No override found and no reset requested – nothing to do
            return

        # Apply the override values
        override_values = self._override_registry[key]
        for field_name, value in override_values.items():
            if hasattr(self, field_name):
                setattr(self, field_name, value)

        # Update the current override key
        self.override_key = key
