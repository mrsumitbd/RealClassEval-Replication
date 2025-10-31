from dataclasses import MISSING, dataclass, fields, is_dataclass
import warnings
import numpy as np

@dataclass
class OverridableConfig:
    """A class that provides an interface to switch between its field values depending on an override key."""

    def __post_init__(self) -> None:
        """Initialize the override key to 'default'."""
        if _OVERRIDE_REGISTRY.get(self.__class__, None) is None:
            _OVERRIDE_REGISTRY[self.__class__] = {}

    def set_override(self, key: str, reset_to_defaults: bool=True) -> None:
        """Set the overridden values for the config based on the override registry.

        Args:
            key: The key to use for the override.
            reset_to_defaults: If True, reset the values to their defaults if no override is found. This is useful for
                when you switch from different non-default overrides to other non-default overrides.
        """
        class_specific_overrides = _OVERRIDE_REGISTRY.get(self.__class__, {})
        active_key_overrides = class_specific_overrides.get(key, {})
        for f in fields(self):
            override_value = active_key_overrides.get(f.name)
            if override_value is not None:
                current_value = getattr(self, f.name, MISSING)
                if current_value != override_value:
                    setattr(self, f.name, override_value)
            elif reset_to_defaults:
                default_value_to_set = MISSING
                if f.default is not MISSING:
                    default_value_to_set = f.default
                elif f.default_factory is not MISSING:
                    default_value_to_set = f.default_factory()
                if default_value_to_set is not MISSING:
                    current_value = getattr(self, f.name, MISSING)
                    if isinstance(current_value, np.ndarray) and isinstance(default_value_to_set, np.ndarray):
                        if not np.array_equal(current_value, default_value_to_set):
                            setattr(self, f.name, default_value_to_set)
                    elif current_value != default_value_to_set:
                        setattr(self, f.name, default_value_to_set)
                else:
                    warnings.warn(f"Field '{f.name}' has no default value to reset to and no override for key '{key}'. Its current value remains unchanged.", UserWarning, stacklevel=2)