from dataclasses import dataclass, asdict, fields
from typing import Any, Dict


@dataclass
class Program:
    '''Represents a program in the database'''

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Program':
        '''Create from dictionary representation'''
        data = data or {}
        field_names = {f.name for f in fields(cls)}
        init_kwargs = {k: v for k, v in data.items() if k in field_names}
        return cls(**init_kwargs)
