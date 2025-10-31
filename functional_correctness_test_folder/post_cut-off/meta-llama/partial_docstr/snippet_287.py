
from dataclasses import dataclass, asdict
from typing import Dict, Any


@dataclass
class InputInterval:
    '''Input interval values to query.'''
    start: int
    end: int

    @classmethod
    def from_dict(cls, data: Dict[str, Any]):
        return cls(**data)

    def __post_init__(self):
        if self.start > self.end:
            raise ValueError("Start value cannot be greater than end value")

    def to_dict(self) -> Dict[str, Any]:
        '''Convert to a dictionary.'''
        return asdict(self)
