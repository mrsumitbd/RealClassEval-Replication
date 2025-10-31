
from dataclasses import dataclass


@dataclass
class OverridableConfig:

    def __post_init__(self) -> None:
        self._overrides = {}

    def set_override(self, key: str, reset_to_defaults: bool = True) -> None:
        if reset_to_defaults:
            self._overrides.pop(key, None)
        else:
            self._overrides[key] = True
