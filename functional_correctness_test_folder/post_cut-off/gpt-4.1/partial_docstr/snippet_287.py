
from dataclasses import dataclass, field
from typing import Any, Dict, Optional


@dataclass
class InputInterval:
    '''Input interval values to query.'''
    start: Optional[Any] = field(default=None)
    end: Optional[Any] = field(default=None)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]):
        return cls(
            start=data.get('start'),
            end=data.get('end')
        )

    def __post_init__(self):
        pass

    def to_dict(self) -> Dict[str, Any]:
        '''Convert to a dictionary.'''
        return {
            'start': self.start,
            'end': self.end
        }
