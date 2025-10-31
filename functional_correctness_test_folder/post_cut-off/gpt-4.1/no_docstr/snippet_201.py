
from dataclasses import dataclass, field
from typing import Any, Dict


@dataclass
class OverridableConfig:
    defaults: Dict[str, Any] = field(default_factory=dict)
    config: Dict[str, Any] = field(default_factory=dict)
    overrides: Dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        self.config = self.defaults.copy()
        self.overrides = {}

    def set_override(self, key: str, reset_to_defaults: bool = True) -> None:
        if key in self.overrides:
            self.config[key] = self.overrides[key]
        elif key in self.defaults:
            self.config[key] = self.defaults[key]
        if reset_to_defaults:
            self.config[key] = self.defaults.get(key, None)
