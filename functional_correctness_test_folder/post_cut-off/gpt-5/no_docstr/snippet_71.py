from dataclasses import dataclass, field
from typing import Any, Callable, List


@dataclass
class HookEvent:
    name: str = ""
    when: str = "after"
    callbacks: List[Callable[..., Any]] = field(default_factory=list)
    _frozen: bool = field(default=False, init=False, repr=False)

    @property
    def should_reverse_callbacks(self) -> bool:
        return self.when.lower() in {"after", "post", "teardown", "exit"}

    def _can_write(self, name: str) -> bool:
        if name.startswith("_"):
            return True
        if not getattr(self, "_frozen", False):
            return True
        return False

    def __post_init__(self) -> None:
        if not isinstance(self.name, str):
            raise TypeError("name must be a string")
        if not isinstance(self.when, str):
            raise TypeError("when must be a string")
        when_norm = self.when.lower()
        if when_norm not in {"before", "pre", "after", "post", "teardown", "exit"}:
            raise ValueError(
                "when must be one of: before, pre, after, post, teardown, exit")
        self.when = when_norm
        if not isinstance(self.callbacks, list):
            raise TypeError("callbacks must be a list")
        for cb in self.callbacks:
            if not callable(cb):
                raise TypeError("each callback must be callable")
        self._frozen = True

    def __setattr__(self, name: str, value: Any) -> None:
        if not self._can_write(name):
            raise AttributeError(
                f"Cannot modify attribute '{name}' after HookEvent is frozen")
        super().__setattr__(name, value)
