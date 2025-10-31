
from dataclasses import dataclass


@dataclass
class Tag:
    name: str
    value: str

    def to_dict(self):
        return {
            'name': self.name,
            'value': self.value
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            name=data['name'],
            value=data['value']
        )
