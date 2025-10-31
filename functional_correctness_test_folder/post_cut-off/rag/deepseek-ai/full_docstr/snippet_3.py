
from dataclasses import dataclass, asdict
from typing import Optional


@dataclass
class StatusBioDTO:
    '''Status biography data transfer object'''
    @classmethod
    def from_model(cls, model: 'StatusBiography') -> 'StatusBioDTO':
        '''Create DTO from database model
        Args:
            model (StatusBiography): database model object
        Returns:
            StatusBioDTO: data transfer object
        '''
        return cls(**model.__dict__)

    def to_dict(self) -> dict:
        '''Convert to dictionary format
        Returns:
            dict: dictionary format data
        '''
        return asdict(self)
