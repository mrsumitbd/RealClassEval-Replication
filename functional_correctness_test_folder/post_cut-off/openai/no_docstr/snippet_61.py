
from dataclasses import dataclass, asdict
from typing import Any, Dict


@dataclass
class Program:
    """
    A generic dataclass that can be serialized to and from a dictionary.
    """

    def to_dict(self) -> Dict[str, Any]:
        """
        Convert the dataclass instance into a dictionary.
        """
        return asdict(self)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Program":
        """
        Create a dataclass instance from a dictionary.
        """
        return cls(**data)
