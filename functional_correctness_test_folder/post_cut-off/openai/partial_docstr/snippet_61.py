
from dataclasses import dataclass, asdict
from typing import Any, Dict


@dataclass
class Program:
    '''Represents a program in the database'''
    id: int
    name: str
    description: str = ""

    def to_dict(self) -> Dict[str, Any]:
        """Return a dictionary representation of the program."""
        return asdict(self)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Program':
        """Create a Program instance from a dictionary."""
        return cls(**data)
