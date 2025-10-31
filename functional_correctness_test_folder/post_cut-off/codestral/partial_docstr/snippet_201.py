
from dataclasses import dataclass


@dataclass
class OverridableConfig:

    def __post_init__(self) -> None:
        '''Initialize the override key to 'default'.'''
        self.override_key = 'default'

    def set_override(self, key: str, reset_to_defaults: bool = True) -> None:
        '''Set the overridden values for the config based on the override registry.
        Args:
            key: The key to use for the override.
            reset_to_defaults: If True, reset the values to their defaults if no override is found. This is useful for
                when you switch from different non-default overrides to other non-default overrides.
        '''
        self.override_key = key
        if reset_to_defaults:
            # Reset to default values if no override is found
            pass
