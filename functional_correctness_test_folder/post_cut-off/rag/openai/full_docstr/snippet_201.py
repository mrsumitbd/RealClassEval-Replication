
from dataclasses import dataclass, field, fields
from typing import Any, Dict


@dataclass
class OverridableConfig:
    """A class that provides an interface to switch between its field values
    depending on an override key.
    """

    # internal state (not part of the public API)
    _override_key: str = field(init=False, repr=False)
    _defaults: Dict[str, Any] = field(init=False, repr=False)

    # registry that maps override keys to field overrides
    _override_registry: Dict[str, Dict[str, Any]] = {}

    def __post_init__(self) -> None:
        """Initialize the override key to 'default' and store the default values."""
        self._override_key = "default"
        # store a copy of the default values for each field
        self._defaults = {f.name: getattr(self, f.name) for f in fields(self)}

    def set_override(self, key: str, reset_to_defaults: bool = True) -> None:
        """
        Set the overridden values for the config based on the override registry.

        Args:
            key: The key to use for the override.
            reset_to_defaults: If True, reset the values to their defaults if no
                override is found. This is useful for when you switch from
                different non-default overrides to other non-default overrides.
        """
        self._override_key = key
        registry = getattr(self.__class__, "_override_registry", {})
        override = registry.get(key)

        # If no override is found
        if override is None:
            if reset_to_defaults:
                # Reset all fields to their original defaults
                for name, value in self._defaults.items():
                    setattr(self, name, value)
            return

        # If an override is found, optionally reset to defaults first
        if reset_to_defaults:
            for name, value in self._defaults.items():
                setattr(self, name, value)

        # Apply the override values
        for name, value in override.items():
            if hasattr(self, name):
                setattr(self, name, value)
