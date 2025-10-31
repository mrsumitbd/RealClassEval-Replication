
from dataclasses import dataclass


@dataclass
class Tag:
    def to_dict(self):
        '''Convert the tag to a dictionary for API requests'''
        return self.__dict__

    @classmethod
    def from_dict(cls, data):
        '''Create a Tag instance from API response data'''
        return cls(**data)
