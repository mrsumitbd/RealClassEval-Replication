
from dataclasses import dataclass, field, fields
from typing import Any, ClassVar, Dict


@dataclass
class OverridableConfig:
    """A class that provides an interface to switch between its field values
    depending on an override key.
    """

    # Class‑level registry that maps override keys to dictionaries of
    # field names → overridden values.
    _override_registry: ClassVar[Dict[str, Dict[str, Any]]] = {}

    # Instance attributes that are not part of the public API.
    _override_key: str = field(init=False, repr=False)
    _defaults: Dict[str, Any] = field(init=False, repr=False)

    def __post_init__(self) -> None:
        """Initialize the override key to 'default' and store the default
        values of all fields.
        """
        self._override_key = "default"
        # Capture the default values of all dataclass fields.
        self._defaults = {f.name: getattr(self, f.name) for f in fields(self)}

    def set_override(self, key: str, reset_to_defaults: bool = True) -> None:
        """Set the overridden values for the config based on the override
        registry.

        Args:
            key: The key to use for the override.
            reset_to_defaults: If True, reset the values to their defaults if
                no override is found. This is useful when switching from one
                non‑default override to another.
        """
        self._override_key = key

        # Retrieve the override mapping for the given key.
        overrides = self.__class__._override_registry.get(key, {})

        # If requested, reset all fields to their original defaults first.
        if reset_to_defaults:
            for name, default_val in self._defaults.items():
                setattr(self, name, default_val)

        # Apply any overrides that exist for this key.
        for name, val in overrides.items():
            if hasattr(self, name):
                setattr(self, name, val)
