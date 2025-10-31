from dataclasses import dataclass, fields, asdict, replace


@dataclass
class OverridableConfig:
    '''A class that provides an interface to switch between its field values depending on an override key.'''

    # Class-level registry for overrides: {key: {field: value, ...}, ...}
    _override_registry: dict = None
    _override_key: str = None
    _defaults: dict = None

    def __post_init__(self) -> None:
        '''Initialize the override key to 'default'.'''
        # Save defaults
        self._defaults = {f.name: getattr(self, f.name) for f in fields(
            self) if not f.name.startswith('_')}
        # Initialize registry if not present
        if self._override_registry is None:
            self._override_registry = {}
        self._override_key = 'default'

    def set_override(self, key: str, reset_to_defaults: bool = True) -> None:
        '''Set the overridden values for the config based on the override registry.
        Args:
            key: The key to use for the override.
            reset_to_defaults: If True, reset the values to their defaults if no override is found. This is useful for
                when you switch from different non-default overrides to other non-default overrides.
        '''
        self._override_key = key
        # Reset to defaults if requested
        if reset_to_defaults:
            for fname, val in self._defaults.items():
                setattr(self, fname, val)
        # Apply override if present
        override = self._override_registry.get(key)
        if override:
            for fname, val in override.items():
                if fname in self._defaults:
                    setattr(self, fname, val)
