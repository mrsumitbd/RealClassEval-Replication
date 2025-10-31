from dataclasses import dataclass, field
from typing import Any, Mapping


@dataclass
class Context:
    data: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        if self.data is None:
            self.data = {}
        elif isinstance(self.data, Mapping):
            self.data = dict(self.data)
        else:
            raise TypeError("data must be a mapping or None")
        for k in self.data.keys():
            if not isinstance(k, str):
                raise TypeError("all keys in data must be strings")

    def __len__(self) -> int:
        return len(self.data)

    def __str__(self) -> str:
        return str(self.data)

    def __repr__(self) -> str:
        return f"Context(data={self.data!r})"

    def to_dict(self) -> dict:
        return dict(self.data)

    @classmethod
    def from_dict(cls, data: dict) -> 'Context':
        if not isinstance(data, Mapping):
            raise TypeError("from_dict expects a mapping")
        return cls(dict(data))
