from dataclasses import dataclass, field, fields
from typing import Any, ClassVar, Dict, Mapping


@dataclass
class OverridableConfig:
    '''A class that provides an interface to switch between its field values depending on an override key.'''

    # Subclasses may define: override_registry: ClassVar[Mapping[str, Mapping[str, Any]]] = {...}
    override_key: str = field(init=False, default="default")
    _defaults: Dict[str, Any] = field(
        init=False, repr=False, default_factory=dict)

    def __post_init__(self) -> None:
        '''Initialize the override key to 'default'.'''
        # Capture default values of all public data fields (exclude internals)
        for f in fields(self):
            if f.name in ("override_key", "_defaults") or f.name.startswith("_"):
                continue
            self._defaults[f.name] = getattr(self, f.name)
        self.override_key = "default"

    def set_override(self, key: str, reset_to_defaults: bool = True) -> None:
        '''Set the overridden values for the config based on the override registry.
        Args:
            key: The key to use for the override.
            reset_to_defaults: If True, reset the values to their defaults if no override is found. This is useful for
                when you switch from different non-default overrides to other non-default overrides.
        '''
        # Fetch override registry from instance or class; default to empty mapping
        registry: Mapping[str, Mapping[str, Any]] = getattr(
            self, "override_registry", {})  # type: ignore[attr-defined]

        if reset_to_defaults:
            for name, value in self._defaults.items():
                setattr(self, name, value)

        if key == "default":
            self.override_key = "default"
            return

        override = registry.get(key)
        if override is not None:
            for name, value in override.items():
                if name in self._defaults:
                    setattr(self, name, value)
            self.override_key = key
        else:
            # No override found
            if reset_to_defaults:
                self.override_key = "default"
            # else keep current override_key unchanged
