
from dataclasses import dataclass
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from models import StatusBiography


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
        return cls(
            # Add attributes from the model here
            # Example: attribute1=model.attribute1,
            #          attribute2=model.attribute2
        )

    def to_dict(self) -> dict:
        '''Convert to dictionary format
        Returns:
            dict: dictionary format data
        '''
        return {
            # Add attributes to the dictionary here
            # Example: 'attribute1': self.attribute1,
            #          'attribute2': self.attribute2
        }
