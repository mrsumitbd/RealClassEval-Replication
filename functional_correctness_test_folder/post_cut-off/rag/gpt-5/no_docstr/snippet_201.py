from dataclasses import dataclass, fields
from typing import Any, Dict, Mapping, Optional
from copy import deepcopy


@dataclass
class OverridableConfig:
    '''A class that provides an interface to switch between its field values depending on an override key.'''

    def __post_init__(self) -> None:
        '''Initialize the override key to 'default'.'''
        object.__setattr__(self, '_override_key', 'default')
        object.__setattr__(self, 'override_key', 'default')
        # Snapshot of default field values to allow resets
        defaults: Dict[str, Any] = {}
        for f in fields(self):
            defaults[f.name] = deepcopy(getattr(self, f.name))
        object.__setattr__(self, '_defaults', defaults)

    def set_override(self, key: str, reset_to_defaults: bool = True) -> None:
        '''Set the overridden values for the config based on the override registry.
        Args:
            key: The key to use for the override.
            reset_to_defaults: If True, reset the values to their defaults if no override is found. This is useful for
                when you switch from different non-default overrides to other non-default overrides.
        '''
        # Resolve registry
        registry: Optional[Mapping[str, Mapping[str, Any]]
                           ] = getattr(self, 'override_registry', None)
        if callable(registry):
            registry = registry()
        if registry is None:
            registry = {}
        # Apply override if present
        override: Optional[Mapping[str, Any]] = registry.get(key)
        if override is None:
            if reset_to_defaults:
                for f in fields(self):
                    setattr(self, f.name, deepcopy(self._defaults[f.name]))
        else:
            # Apply only known fields from override
            field_names = {f.name for f in fields(self)}
            for name, value in override.items():
                if name in field_names:
                    setattr(self, name, value)
        # Update current override key
        object.__setattr__(self, '_override_key', key)
        object.__setattr__(self, 'override_key', key)
