
from dataclasses import dataclass, fields
from typing import Any


@dataclass
class HookEvent:
    def should_reverse_callbacks(self) -> bool:
        return False

    def _can_write(self, name: str) -> bool:
        return name in [f.name for f in fields(self)]

    def __post_init__(self) -> None:
        for name, value in self.__dict__.items():
            if not self._can_write(name):
                raise AttributeError(f"Cannot set attribute {name}")

    def __setattr__(self, name: str, value: Any) -> None:
        if not self._can_write(name):
            raise AttributeError("Cannot set attribute on hook event")
        super().__setattr__(name, value)
