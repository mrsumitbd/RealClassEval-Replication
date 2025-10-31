
from dataclasses import dataclass, asdict, fields
from typing import Dict, Any


@dataclass
class Program:
    '''Represents a program in the database'''
    # Assuming the class has some attributes, for example:
    id: int
    name: str
    description: str

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Program':
        '''Create from dictionary representation'''
        field_names = {f.name for f in fields(cls)}
        filtered_data = {k: v for k, v in data.items() if k in field_names}
        return cls(**filtered_data)
