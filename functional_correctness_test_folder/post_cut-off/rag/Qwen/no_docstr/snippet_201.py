
from dataclasses import dataclass, fields
from typing import Any, Dict


@dataclass
class OverridableConfig:
    '''A class that provides an interface to switch between its field values depending on an override key.'''

    _override_key: str = 'default'
    _overrides: Dict[str, Dict[str, Any]] = None

    def __post_init__(self) -> None:
        '''Initialize the override key to 'default' and prepare the overrides dictionary.'''
        self._overrides = {field.name: {} for field in fields(self)}

    def set_override(self, key: str, reset_to_defaults: bool = True) -> None:
        '''Set the overridden values for the config based on the override registry.
        Args:
            key: The key to use for the override.
            reset_to_defaults: If True, reset the values to their defaults if no override is found. This is useful for
                when you switch from different non-default overrides to other non-default overrides.
        '''
        self._override_key = key
        for field in fields(self):
            if key in self._overrides[field.name]:
                setattr(self, field.name, self._overrides[field.name][key])
            elif reset_to_defaults:
                setattr(self, field.name, field.default)

    def register_override(self, field_name: str, key: str, value: Any) -> None:
        '''Register an override value for a specific field and key.
        Args:
            field_name: The name of the field to override.
            key: The key under which to store the override.
            value: The value to use as the override.
        '''
        if field_name in self._overrides:
            self._overrides[field_name][key] = value
        else:
            raise ValueError(
                f"Field '{field_name}' does not exist in the config.")
