
from dataclasses import dataclass, asdict


@dataclass
class Tag:
    id: int
    name: str

    def to_dict(self):
        '''Convert the tag to a dictionary for API requests'''
        return asdict(self)

    @classmethod
    def from_dict(cls, data):
        '''Create a Tag instance from API response data'''
        return cls(**data)
