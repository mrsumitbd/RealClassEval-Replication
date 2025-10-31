
from dataclasses import dataclass, asdict


@dataclass
class Tag:
    def to_dict(self):
        return asdict(self)

    @classmethod
    def from_dict(cls, data):
        return cls(**data)
