
from dataclasses import dataclass, field
from typing import Any, Dict, ClassVar


@dataclass
class OverridableConfig:
    # Class-level registry for overrides: {key: {attr: value, ...}}
    _override_registry: ClassVar[Dict[str, Dict[str, Any]]] = {}

    # Store the current override key
    _override_key: str = field(init=False, default='default')

    def __post_init__(self) -> None:
        '''Initialize the override key to 'default'.'''
        self._override_key = 'default'

    def set_override(self, key: str, reset_to_defaults: bool = True) -> None:
        '''Set the overridden values for the config based on the override registry.'''
        cls = self.__class__
        # Get the override dict for the key, if any
        override = cls._override_registry.get(key)
        if reset_to_defaults:
            # Reset all fields to their default values
            for f in self.__dataclass_fields__.values():
                if f.name.startswith('_'):
                    continue
                if f.default is not dataclass._MISSING_TYPE:
                    setattr(self, f.name, f.default)
                elif f.default_factory is not dataclass._MISSING_TYPE:  # type: ignore
                    setattr(self, f.name, f.default_factory())
        if override:
            for k, v in override.items():
                if k in self.__dataclass_fields__:
                    setattr(self, k, v)
        self._override_key = key
