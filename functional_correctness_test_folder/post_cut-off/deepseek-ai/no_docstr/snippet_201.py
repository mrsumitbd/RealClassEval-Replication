
from dataclasses import dataclass, field
from typing import Any, Dict


@dataclass
class OverridableConfig:
    _overrides: Dict[str, Any] = field(default_factory=dict, init=False)

    def __post_init__(self) -> None:
        self._defaults = {k: v for k,
                          v in self.__dict__.items() if not k.startswith('_')}

    def set_override(self, key: str, reset_to_defaults: bool = True) -> None:
        if reset_to_defaults:
            if key in self._defaults:
                setattr(self, key, self._defaults[key])
            if key in self._overrides:
                del self._overrides[key]
        else:
            if key in self.__dict__ and not key.startswith('_'):
                self._overrides[key] = getattr(self, key)
