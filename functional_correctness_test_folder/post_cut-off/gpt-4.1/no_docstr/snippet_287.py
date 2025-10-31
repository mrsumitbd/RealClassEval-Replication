
from dataclasses import dataclass, field
from typing import Any, Dict, Optional


@dataclass
class InputInterval:
    start: Optional[float] = field(default=None)
    end: Optional[float] = field(default=None)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]):
        return cls(
            start=data.get('start'),
            end=data.get('end')
        )

    def __post_init__(self):
        if self.start is not None and self.end is not None:
            if self.start > self.end:
                raise ValueError("start must not be greater than end")

    def to_dict(self) -> Dict[str, Any]:
        return {
            'start': self.start,
            'end': self.end
        }
