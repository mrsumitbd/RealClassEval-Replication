
from dataclasses import dataclass


@dataclass
class Tag:
    id: int = None
    name: str = None

    def to_dict(self):
        '''Convert the tag to a dictionary for API requests'''
        result = {}
        if self.id is not None:
            result['id'] = self.id
        if self.name is not None:
            result['name'] = self.name
        return result

    @classmethod
    def from_dict(cls, data):
        '''Create a Tag instance from API response data'''
        id_ = data.get('id')
        name = data.get('name')
        return cls(id=id_, name=name)
