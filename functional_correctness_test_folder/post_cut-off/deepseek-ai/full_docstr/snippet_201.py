
from dataclasses import dataclass, fields
from typing import Any, Dict


@dataclass
class OverridableConfig:
    '''A class that provides an interface to switch between its field values depending on an override key.'''
    _override_registry: Dict[str, Dict[str, Any]] = None
    _override_key: str = 'default'

    def __post_init__(self) -> None:
        '''Initialize the override key to 'default'.'''
        self._override_registry = {}
        self._override_key = 'default'

    def set_override(self, key: str, reset_to_defaults: bool = True) -> None:
        '''Set the overridden values for the config based on the override registry.
        Args:
            key: The key to use for the override.
            reset_to_defaults: If True, reset the values to their defaults if no override is found. This is useful for
                when you switch from different non-default overrides to other non-default overrides.
        '''
        if key not in self._override_registry:
            if reset_to_defaults:
                # Reset to default values
                default_overrides = self._override_registry.get('default', {})
                for field in fields(self):
                    if field.name not in ['_override_registry', '_override_key']:
                        setattr(self, field.name, default_overrides.get(
                            field.name, getattr(self, field.name)))
            return

        overrides = self._override_registry[key]
        for field_name, value in overrides.items():
            if hasattr(self, field_name):
                setattr(self, field_name, value)
        self._override_key = key
