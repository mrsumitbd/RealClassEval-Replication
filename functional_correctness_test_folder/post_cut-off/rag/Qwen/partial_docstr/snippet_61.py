
from dataclasses import dataclass
from typing import Any, Dict


@dataclass
class Program:
    '''Represents a program in the database'''
    name: str
    version: str
    description: str
    author: str

    def to_dict(self) -> Dict[str, Any]:
        '''Convert to dictionary representation'''
        return {
            'name': self.name,
            'version': self.version,
            'description': self.description,
            'author': self.author
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Program':
        '''Create from dictionary representation'''
        return cls(
            name=data['name'],
            version=data['version'],
            description=data['description'],
            author=data['author']
        )
