
from dataclasses import dataclass, field


@dataclass
class Context:
    data: dict = field(default_factory=dict)

    def __post_init__(self) -> None:
        if not isinstance(self.data, dict):
            raise TypeError("data must be a dictionary")

    def __len__(self) -> int:
        return len(self.data)

    def __str__(self) -> str:
        return str(self.data)

    def __repr__(self) -> str:
        return f"Context(data={repr(self.data)})"

    def to_dict(self) -> dict:
        return dict(self.data)

    @classmethod
    def from_dict(cls, data: dict) -> 'Context':
        return cls(data=dict(data))
