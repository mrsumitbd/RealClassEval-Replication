
from dataclasses import dataclass, asdict


@dataclass
class Tag:
    id: int
    name: str

    def to_dict(self):
        return asdict(self)

    @classmethod
    def from_dict(cls, data):
        return cls(**data)
