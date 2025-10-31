
from dataclasses import dataclass, fields
from typing import Any, Dict


@dataclass
class OverridableConfig:
    _override_key: str = 'default'
    _override_registry: Dict[str, Dict[str, Any]] = None

    def __post_init__(self) -> None:
        self._override_key = 'default'
        self._override_registry = {}

    def set_override(self, key: str, reset_to_defaults: bool = True) -> None:
        if reset_to_defaults:
            for field in fields(self):
                setattr(self, field.name, field.default)
        if key in self._override_registry:
            for field_name, value in self._override_registry[key].items():
                setattr(self, field_name, value)
        self._override_key = key
