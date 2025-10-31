
from dataclasses import dataclass, asdict
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    # Replace 'your_module' with the actual module name
    from your_module import StatusBiography


@dataclass
class StatusBioDTO:
    '''Status biography data transfer object'''
    # Assuming StatusBiography has the following attributes
    id: int
    biography: str

    @classmethod
    def from_model(cls, model: 'StatusBiography') -> 'StatusBioDTO':
        '''Create DTO from database model
        Args:
            model (StatusBiography): database model object
        Returns:
            StatusBioDTO: data transfer object
        '''
        return cls(id=model.id, biography=model.biography)

    def to_dict(self) -> dict:
        '''Convert to dictionary format
        Returns:
            dict: dictionary format data
        '''
        return asdict(self)
