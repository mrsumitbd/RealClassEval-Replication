
from dataclasses import dataclass, fields, asdict
from typing import Dict, Any


@dataclass
class OverridableConfig:
    '''A class that provides an interface to switch between its field values depending on an override key.'''

    _override_key: str = 'default'
    _override_registry: Dict[str, Dict[str, Any]] = None

    def __post_init__(self) -> None:
        '''Initialize the override key to 'default'.'''
        self._override_key = 'default'
        self._override_registry = {}

    def set_override(self, key: str, reset_to_defaults: bool = True) -> None:
        '''Set the overridden values for the config based on the override registry.
        Args:
            key: The key to use for the override.
            reset_to_defaults: If True, reset the values to their defaults if no override is found. This is useful for
                when you switch from different non-default overrides to other non-default overrides.
        '''
        if key in self._override_registry:
            override_values = self._override_registry[key]
            for field_name, field_value in override_values.items():
                if hasattr(self, field_name):
                    setattr(self, field_name, field_value)
        elif reset_to_defaults:
            default_values = asdict(self)
            for field in fields(self):
                if field.name != '_override_key' and field.name != '_override_registry':
                    setattr(self, field.name, default_values[field.name])
        self._override_key = key

    def register_override(self, key: str, values: Dict[str, Any]) -> None:
        '''Register an override for a specific key.
        Args:
            key: The key to register the override for.
            values: A dictionary of field names to their overridden values.
        '''
        self._override_registry[key] = values
