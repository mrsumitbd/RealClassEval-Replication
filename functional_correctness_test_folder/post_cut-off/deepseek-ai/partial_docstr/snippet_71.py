
from dataclasses import dataclass
from typing import Any


@dataclass
class HookEvent:
    @property
    def should_reverse_callbacks(self) -> bool:
        return False

    def _can_write(self, name: str) -> bool:
        return False

    def __post_init__(self) -> None:
        object.__setattr__(self, '_initialized', True)

    def __setattr__(self, name: str, value: Any) -> None:
        if not self._can_write(name):
            raise AttributeError(f"Cannot set attribute '{name}' on HookEvent")
        object.__setattr__(self, name, value)
