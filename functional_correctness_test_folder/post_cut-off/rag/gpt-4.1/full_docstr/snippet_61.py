from dataclasses import dataclass, asdict, fields
from typing import Any, Dict


@dataclass
class Program:
    '''Represents a program in the database'''

    id: int
    name: str
    description: str
    is_active: bool

    def to_dict(self) -> Dict[str, Any]:
        '''Convert to dictionary representation'''
        return asdict(self)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Program':
        '''Create from dictionary representation'''
        field_names = {f.name for f in fields(cls)}
        filtered_data = {k: v for k, v in data.items() if k in field_names}
        return cls(**filtered_data)
