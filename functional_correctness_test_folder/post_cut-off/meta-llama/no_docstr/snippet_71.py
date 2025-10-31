
from dataclasses import dataclass, field
from typing import Any


@dataclass
class HookEvent:
    _frozen: bool = field(default=False, init=False, repr=False)

    @property
    def should_reverse_callbacks(self) -> bool:
        return False

    def _can_write(self, name: str) -> bool:
        return not self._frozen

    def __post_init__(self) -> None:
        self._frozen = True

    def __setattr__(self, name: str, value: Any) -> None:
        if self._can_write(name):
            super().__setattr__(name, value)
        else:
            raise AttributeError(
                f"Cannot modify attribute '{name}' after initialization")
