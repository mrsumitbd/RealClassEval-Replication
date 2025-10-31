
from dataclasses import dataclass, fields, MISSING
from typing import Any, Dict, Optional


@dataclass
class OverridableConfig:
    '''A class that provides an interface to switch between its field values depending on an override key.'''

    # The override key is stored as a private attribute
    _override_key: str = "default"

    def __post_init__(self) -> None:
        '''Initialize the override key to 'default'.'''
        # Ensure the override key is set to the default value
        self._override_key = "default"

    def set_override(self, key: str, reset_to_defaults: bool = True) -> None:
        '''Set the overridden values for the config based on the override registry.
        Args:
            key: The key to use for the override.
            reset_to_defaults: If True, reset the values to their defaults if no override is found. This is useful for
                when you switch from different non-default overrides to other non-default overrides.
        '''
        # Store the override key
        self._override_key = key

        # Retrieve the override registry from the class, if it exists
        registry: Dict[str, Dict[str, Any]] = getattr(
            self.__class__, "_override_registry", {})

        # Get the override values for the requested key
        override_values: Optional[Dict[str, Any]] = registry.get(key)

        # If no override values are found
        if override_values is None:
            if reset_to_defaults:
                # Reset all fields to their default values
                for f in fields(self):
                    if f.name.startswith("_"):
                        continue  # skip private attributes
                    if f.default is not MISSING:
                        setattr(self, f.name, f.default)
                    # type: ignore[arg-type]
                    elif f.default_factory is not MISSING:
                        # type: ignore[arg-type]
                        setattr(self, f.name, f.default_factory())
                    else:
                        # No default; leave as is
                        pass
            # Nothing else to do if no override and no reset
            return

        # Apply override values
        for f in fields(self):
            if f.name.startswith("_"):
                continue  # skip private attributes
            if f.name in override_values:
                setattr(self, f.name, override_values[f.name])
            elif reset_to_defaults:
                # Reset to default if not overridden
                if f.default is not MISSING:
                    setattr(self, f.name, f.default)
                # type: ignore[arg-type]
                elif f.default_factory is not MISSING:
                    # type: ignore[arg-type]
                    setattr(self, f.name, f.default_factory())
                else:
                    # No default; leave as is
                    pass
