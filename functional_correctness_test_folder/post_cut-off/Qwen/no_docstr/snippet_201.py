
from dataclasses import dataclass, field
from typing import Any, Dict


@dataclass
class OverridableConfig:
    _defaults: Dict[str, Any] = field(init=False, default_factory=dict)
    _overrides: Dict[str, Any] = field(init=False, default_factory=dict)

    def __post_init__(self) -> None:
        self._defaults = {field.name: getattr(
            self, field.name) for field in self.__dataclass_fields__.values()}
        self._overrides = {}

    def set_override(self, key: str, value: Any, reset_to_defaults: bool = False) -> None:
        if reset_to_defaults:
            if key in self._overrides:
                del self._overrides[key]
            setattr(self, key, self._defaults.get(key, None))
        else:
            self._overrides[key] = value
            setattr(self, key, value)
