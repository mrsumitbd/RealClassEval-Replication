
from dataclasses import dataclass, field
from typing import Any, Dict


@dataclass
class InputInterval:
    start: int
    end: int

    @classmethod
    def from_dict(cls, data: Dict[str, Any]):
        return cls(**data)

    def __post_init__(self):
        if self.start > self.end:
            raise ValueError("Start must be less than or equal to end")

    def to_dict(self) -> Dict[str, Any]:
        return {
            'start': self.start,
            'end': self.end
        }
