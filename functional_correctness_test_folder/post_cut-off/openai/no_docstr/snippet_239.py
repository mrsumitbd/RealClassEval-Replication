
from dataclasses import dataclass, asdict


@dataclass
class Tag:
    """
    A simple dataclass that can be converted to and from a dictionary.
    """

    def to_dict(self):
        """
        Convert the dataclass instance into a dictionary.
        """
        return asdict(self)

    @classmethod
    def from_dict(cls, data):
        """
        Create an instance of the dataclass from a dictionary.
        """
        return cls(**data)
