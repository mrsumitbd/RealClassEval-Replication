
from dataclasses import dataclass, asdict
from typing import Any, Dict, Optional


@dataclass
class Program:
    '''Represents a program in the database'''
    id: int
    name: str
    description: Optional[str] = None
    version: Optional[str] = None
    created_at: Optional[str] = None
    updated_at: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        '''Convert to dictionary representation'''
        return asdict(self)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Program':
        '''Create from dictionary representation'''
        return cls(**data)
