
from dataclasses import dataclass, field, fields, asdict, MISSING
from typing import Any, Dict, ClassVar


@dataclass
class OverridableConfig:
    '''A class that provides an interface to switch between its field values depending on an override key.'''

    # Class-level registry for overrides: {key: {field_name: value, ...}}
    _override_registry: ClassVar[Dict[str, Dict[str, Any]]] = {}

    # Instance-level current override key
    _override_key: str = field(init=False, repr=False, default='default')

    def __post_init__(self) -> None:
        '''Initialize the override key to 'default'.'''
        self._override_key = 'default'

    def set_override(self, key: str, reset_to_defaults: bool = True) -> None:
        '''Set the overridden values for the config based on the override registry.
        Args:
            key: The key to use for the override.
            reset_to_defaults: If True, reset the values to their defaults if no override is found. This is useful for
                when you switch from different non-default overrides to other non-default overrides.
        '''
        # Get all dataclass fields except private ones
        config_fields = [f for f in fields(self) if not f.name.startswith('_')]

        # If reset_to_defaults, set all fields to their default values
        if reset_to_defaults:
            for f in config_fields:
                if f.default is not MISSING:
                    setattr(self, f.name, f.default)
                elif f.default_factory is not MISSING:  # type: ignore
                    setattr(self, f.name, f.default_factory())  # type: ignore

        # Apply override if present
        override = self._override_registry.get(key)
        if override:
            for name, value in override.items():
                if hasattr(self, name):
                    setattr(self, name, value)

        self._override_key = key

    @classmethod
    def register_override(cls, key: str, values: Dict[str, Any]) -> None:
        '''Register an override for a given key.'''
        cls._override_registry[key] = values
