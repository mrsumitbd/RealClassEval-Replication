from dataclasses import dataclass, fields, Field
from typing import Any, Dict, ClassVar, Mapping
import copy


@dataclass
class OverridableConfig:
    # Optional class-level override registry; subclasses may override
    OVERRIDES: ClassVar[Mapping[str, Mapping[str, Any]]] = {}

    # Internal state (excluded from dataclass initialization/comparison)
    _override_key: str = None  # type: ignore
    _override_registry: Dict[str, Dict[str, Any]] = None  # type: ignore
    _defaults_snapshot: Dict[str, Any] = None  # type: ignore

    def __post_init__(self) -> None:
        '''Initialize the override key to 'default'.'''
        # Initialize internal registries/state
        object.__setattr__(self, "_override_key", "default")
        # Prepare the registry (instance attribute `override_registry` or class-level OVERRIDES)
        registry: Mapping[str, Mapping[str, Any]] = getattr(
            self, "override_registry", None)  # type: ignore
        if registry is None:
            registry = self.OVERRIDES or {}
        # Normalize to dict of dicts
        norm_registry: Dict[str, Dict[str, Any]] = {}
        for k, v in dict(registry).items():
            norm_registry[str(k)] = dict(v)
        object.__setattr__(self, "_override_registry", norm_registry)

        # Snapshot defaults for overridable fields
        defaults: Dict[str, Any] = {}
        for f in fields(self):
            if self._is_overridable_field(f):
                defaults[f.name] = copy.deepcopy(getattr(self, f.name))
        object.__setattr__(self, "_defaults_snapshot", defaults)

    def set_override(self, key: str, reset_to_defaults: bool = True) -> None:
        '''Set the overridden values for the config based on the override registry.
        Args:
            key: The key to use for the override.
            reset_to_defaults: If True, reset the values to their defaults if no override is found. This is useful for
                when you switch from different non-default overrides to other non-default overrides.
        '''
        # Select base state: defaults or current
        if reset_to_defaults:
            for name, val in self._defaults_snapshot.items():
                setattr(self, name, copy.deepcopy(val))

        overrides = self._override_registry.get(key)
        if overrides is not None:
            for name, value in overrides.items():
                if not self._is_overridable_name(name):
                    continue
                resolved = value(self) if callable(value) else value
                setattr(self, name, resolved)
        else:
            if reset_to_defaults:
                # Already reset to defaults; nothing more to do
                pass

        object.__setattr__(self, "_override_key", key)

    @staticmethod
    def _is_overridable_field(f: Field) -> bool:
        # Exclude private/internal, ClassVars, and fields with init=False and repr=False that are clearly internal
        if f.name.startswith("_"):
            return False
        if getattr(f.type, "__origin__", None) is ClassVar:
            return False
        return True

    @staticmethod
    def _is_overridable_name(name: str) -> bool:
        return not name.startswith("_")
