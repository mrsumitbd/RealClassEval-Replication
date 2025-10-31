
from dataclasses import dataclass, fields


@dataclass
class OverridableConfig:
    _override_key: str = 'default'

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
        self._override_key = key
        if reset_to_defaults:
            for field in fields(self):
                if hasattr(self, f'_default_{field.name}'):
                    setattr(self, field.name, getattr(
                        self, f'_default_{field.name}'))
