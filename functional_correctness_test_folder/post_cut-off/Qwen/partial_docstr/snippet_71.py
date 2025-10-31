
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
        for field in self.__dataclass_fields__:
            if not self._can_write(field):
                object.__setattr__(self, field, getattr(self, field))

    def __setattr__(self, name: str, value: Any) -> None:
        raise AttributeError("Cannot set attributes on hook events.")
