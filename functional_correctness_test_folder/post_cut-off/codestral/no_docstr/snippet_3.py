
from dataclasses import dataclass


@dataclass
class StatusBioDTO:

    @classmethod
    def from_model(cls, model: 'StatusBiography') -> 'StatusBioDTO':
        return cls()

    def to_dict(self) -> dict:
        return self.__dict__
