
from dataclasses import dataclass, field
from typing import Any


@dataclass
class HookEvent:
    _should_reverse_callbacks: bool = field(
        default=False, repr=False, init=False)
    _locked: bool = field(default=False, repr=False, init=False)

    @property
    def should_reverse_callbacks(self) -> bool:
        return self._should_reverse_callbacks

    def _can_write(self, name: str) -> bool:
        # Allow writing before __post_init__ locks, or always allow for private attributes
        if name.startswith('_'):
            return True
        return not self._locked

    def __post_init__(self) -> None:
        # Lock the instance after initialization
        self._locked = True

    def __setattr__(self, name: str, value: Any) -> None:
        if not self._can_write(name):
            raise AttributeError(
                f"Cannot set attribute '{name}' after initialization")
        super().__setattr__(name, value)
