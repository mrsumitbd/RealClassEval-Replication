
from dataclasses import dataclass, field
from typing import Any, Dict


@dataclass
class HookEvent:
    _callbacks_reversed: bool = field(default=False, init=False)
    _writable_attributes: Dict[str, bool] = field(
        default_factory=dict, init=False)

    @property
    def should_reverse_callbacks(self) -> bool:
        return self._callbacks_reversed

    def _can_write(self, name: str) -> bool:
        return self._writable_attributes.get(name, False)

    def __post_init__(self) -> None:
        self._writable_attributes = {field.name: field.metadata.get(
            'writable', False) for field in self.__dataclass_fields__.values()}

    def __setattr__(self, name: str, value: Any) -> None:
        if not self._can_write(name):
            raise AttributeError(f"Attribute '{name}' is not writable.")
        super().__setattr__(name, value)
