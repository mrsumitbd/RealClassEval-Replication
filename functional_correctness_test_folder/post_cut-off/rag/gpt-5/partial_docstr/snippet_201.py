from dataclasses import dataclass, field, fields
from typing import Any, Dict, Mapping
from copy import deepcopy


@dataclass
class OverridableConfig:
    '''A class that provides an interface to switch between its field values depending on an override key.'''

    _override_key: str = field(init=False, default='default', repr=False)
    _default_values: Dict[str, Any] = field(
        init=False, default_factory=dict, repr=False)

    def __post_init__(self) -> None:
        '''Initialize the override key to 'default'.'''
        self._override_key = 'default'
        # Snapshot defaults from current instance state
        for f in fields(self):
            name = f.name
            if name.startswith('_'):
                continue
            self._default_values[name] = deepcopy(getattr(self, name, None))

    def _get_override_registry(self) -> Mapping[str, Mapping[str, Any]]:
        # Prefer instance attribute 'override_registry', then class attribute, fall back to 'overrides'
        registry = getattr(self, 'override_registry', None)
        if registry is None:
            registry = getattr(self.__class__, 'override_registry', None)
        if registry is None:
            registry = getattr(self, 'overrides', None)
        if registry is None:
            registry = getattr(self.__class__, 'overrides', None)
        return registry or {}

    def _reset_to_defaults(self) -> None:
        for name, value in self._default_values.items():
            setattr(self, name, deepcopy(value))

    def set_override(self, key: str, reset_to_defaults: bool = True) -> None:
        '''Set the overridden values for the config based on the override registry.
        Args:
            key: The key to use for the override.
            reset_to_defaults: If True, reset the values to their defaults if no override is found. This is useful for
                when you switch from different non-default overrides to other non-default overrides.
        '''
        registry = self._get_override_registry()
        overrides = registry.get(key)

        # Reset to defaults first to avoid stale values when switching overrides.
        if reset_to_defaults:
            self._reset_to_defaults()

        if overrides:
            valid_fields = {f.name for f in fields(
                self) if not f.name.startswith('_')}
            for name, value in overrides.items():
                if name in valid_fields:
                    setattr(self, name, deepcopy(value))

        self._override_key = key
