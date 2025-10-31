
from dataclasses import dataclass
from typing import Dict, Any


@dataclass
class InputInterval:
    start: int
    end: int

    @classmethod
    def from_dict(cls, data: Dict[str, Any]):
        return cls(**data)

    def __post_init__(self):
        if self.start > self.end:
            self.start, self.end = self.end, self.start

    def to_dict(self) -> Dict[str, Any]:
        return {'start': self.start, 'end': self.end}
