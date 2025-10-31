from dataclasses import dataclass, fields, asdict, replace


@dataclass
class OverridableConfig:
    '''A class that provides an interface to switch between its field values depending on an override key.'''

    # Registry of overrides: {key: {field: value, ...}, ...}
    _override_registry: dict = None
    _override_key: str = None
    _defaults: dict = None

    def __post_init__(self) -> None:
        '''Initialize the override key to 'default'.'''
        object.__setattr__(self, '_override_key', 'default')
        if self._override_registry is None:
            object.__setattr__(self, '_override_registry', {})
        # Save defaults for all fields except private ones
        defaults = {}
        for f in fields(self):
            if not f.name.startswith('_'):
                defaults[f.name] = getattr(self, f.name)
        object.__setattr__(self, '_defaults', defaults)

    def set_override(self, key: str, reset_to_defaults: bool = True) -> None:
        '''Set the overridden values for the config based on the override registry.
        Args:
            key: The key to use for the override.
            reset_to_defaults: If True, reset the values to their defaults if no override is found. This is useful for
                when you switch from different non-default overrides to other non-default overrides.
        '''
        self._override_key = key
        override = self._override_registry.get(key)
        if override is not None:
            for fname, value in override.items():
                if hasattr(self, fname):
                    setattr(self, fname, value)
        elif reset_to_defaults:
            for fname, value in self._defaults.items():
                setattr(self, fname, value)
