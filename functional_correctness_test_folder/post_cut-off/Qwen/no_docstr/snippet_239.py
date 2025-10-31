
from dataclasses import dataclass, asdict


@dataclass
class Tag:
    name: str
    value: str

    def to_dict(self):
        return asdict(self)

    @classmethod
    def from_dict(cls, data):
        return cls(**data)
