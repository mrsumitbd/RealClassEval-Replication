
from dataclasses import dataclass, asdict
from typing import Dict, Any


@dataclass
class Program:
    '''Represents a program in the database'''

    def to_dict(self) -> Dict[str, Any]:
        '''Convert to dictionary representation'''
        return asdict(self)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Program':
        '''Create from dictionary representation'''
        return cls(**data)
