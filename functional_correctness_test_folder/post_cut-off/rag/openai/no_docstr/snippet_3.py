
from dataclasses import dataclass
from typing import Any, Dict


@dataclass
class StatusBioDTO:
    '''Status biography data transfer object'''

    @classmethod
    def from_model(cls, model: Any) -> 'StatusBioDTO':
        '''Create DTO from database model
        Args:
            model (StatusBiography): database model object
        Returns:
            StatusBioDTO: data transfer object
        '''
        dto = cls()
        # Copy all public attributes from the model to the DTO
        for key, value in vars(model).items():
            if not key.startswith('_'):
                setattr(dto, key, value)
        return dto

    def to_dict(self) -> Dict[str, Any]:
        '''Convert to dictionary format
        Returns:
            dict: dictionary format data
        '''
        # Return a shallow copy of the DTO's __dict__
        return {k: v for k, v in self.__dict__.items() if not k.startswith('_')}
