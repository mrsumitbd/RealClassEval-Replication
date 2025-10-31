
from dataclasses import dataclass
from typing import Any


@dataclass
class HookEvent:
    _should_reverse_callbacks: bool = False

    @property
    def should_reverse_callbacks(self) -> bool:
        return self._should_reverse_callbacks

    def _can_write(self, name: str) -> bool:
        return not name.startswith('_')

    def __post_init__(self) -> None:
        pass

    def __setattr__(self, name: str, value: Any) -> None:
        if self._can_write(name):
            super().__setattr__(name, value)
        else:
            raise AttributeError(f"Cannot set attribute '{name}'")
