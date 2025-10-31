from dataclasses import dataclass, field
from typing import Any, Dict
import copy


@dataclass
class OverridableConfig:
    _defaults: Dict[str, Any] = field(init=False, repr=False)
    _overrides: Dict[str, Any] = field(default_factory=dict, repr=False)

    def __post_init__(self) -> None:
        public_items = {
            k: v for k, v in vars(self).items()
            if not k.startswith('_') and not callable(v)
        }
        object.__setattr__(self, "_defaults", copy.deepcopy(public_items))

    def set_override(self, key: str, reset_to_defaults: bool = True) -> None:
        if key not in self._defaults:
            raise KeyError(f"Unknown config key: {key}")
        current_value = getattr(self, key)
        self._overrides[key] = current_value
        if reset_to_defaults:
            setattr(self, key, copy.deepcopy(self._defaults[key]))
