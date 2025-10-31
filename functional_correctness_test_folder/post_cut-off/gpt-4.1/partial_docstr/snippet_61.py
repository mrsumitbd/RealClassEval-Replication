
from dataclasses import dataclass, asdict
from typing import Dict, Any


@dataclass
class Program:
    '''Represents a program in the database'''
    name: str
    version: str
    description: str = ""
    author: str = ""

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Program':
        return cls(
            name=data.get('name', ''),
            version=data.get('version', ''),
            description=data.get('description', ''),
            author=data.get('author', '')
        )
