from dataclasses import dataclass, field, fields as dataclass_fields
from typing import Any, Dict, Mapping, Set
from copy import deepcopy


@dataclass
class OverridableConfig:
    '''A class that provides an interface to switch between its field values depending on an override key.'''

    # Registry mapping override keys to dicts of field overrides
    override_registry: Dict[str, Dict[str, Any]] = field(default_factory=dict)

    # Internal state
    _defaults: Dict[str, Any] = field(
        init=False, repr=False, default_factory=dict)
    _managed_fields: Set[str] = field(
        init=False, repr=False, default_factory=set)
    _override_key: str = field(init=False, repr=False, default='default')

    def __post_init__(self) -> None:
        '''Initialize the override key to 'default'.'''
        self._override_key = 'default'
        # Determine which fields are managed (exclude internal/private fields and the registry itself)
        self._managed_fields = {
            f.name
            for f in dataclass_fields(self)
            if not f.name.startswith('_') and f.name != 'override_registry'
        }
        # Capture defaults snapshot
        for name in self._managed_fields:
            self._defaults[name] = deepcopy(getattr(self, name))

    def set_override(self, key: str, reset_to_defaults: bool = True) -> None:
        '''Set the overridden values for the config based on the override registry.
        Args:
            key: The key to use for the override.
            reset_to_defaults: If True, reset the values to their defaults if no override is found. This is useful for
                when you switch from different non-default overrides to other non-default overrides.
        '''
        registry: Mapping[str, Dict[str, Any]] = getattr(
            self, 'override_registry', {}) or {}
        overrides = registry.get(key)

        if reset_to_defaults:
            # Reset to captured defaults before applying any override
            for name in self._managed_fields:
                setattr(self, name, deepcopy(self._defaults[name]))

        if overrides:
            for name, value in overrides.items():
                if name in self._managed_fields:
                    setattr(self, name, deepcopy(value))

        elif overrides is None and not reset_to_defaults:
            # If no overrides found and we are not resetting to defaults,
            # do nothing (retain current values)
            pass

        self._override_key = key
