
from dataclasses import dataclass, fields, MISSING
from typing import Dict, Any


@dataclass
class OverridableConfig:
    '''A class that provides an interface to switch between its field values depending on an override key.'''

    _override_registry: Dict[str, Dict[str, Any]] = None
    _override_key: str = 'default'

    def __post_init__(self) -> None:
        '''Initialize the override key to 'default'.'''
        if self._override_registry is None:
            self._override_registry = {}
            for field in fields(self):
                if field.metadata is not None and 'overrides' in field.metadata:
                    for key, value in field.metadata['overrides'].items():
                        if key not in self._override_registry:
                            self._override_registry[key] = {}
                        self._override_registry[key][field.name] = value
        self._override_key = 'default'

    def set_override(self, key: str, reset_to_defaults: bool = True) -> None:
        '''Set the overridden values for the config based on the override registry.
        Args:
            key: The key to use for the override.
            reset_to_defaults: If True, reset the values to their defaults if no override is found. This is useful for
                when you switch from different non-default overrides to other non-default overrides.
        '''
        if reset_to_defaults:
            for field in fields(self):
                if field.default is not MISSING:
                    setattr(self, field.name, field.default)
                elif field.default_factory is not MISSING:
                    setattr(self, field.name, field.default_factory())

        if key in self._override_registry:
            for field_name, value in self._override_registry[key].items():
                setattr(self, field_name, value)
        self._override_key = key
