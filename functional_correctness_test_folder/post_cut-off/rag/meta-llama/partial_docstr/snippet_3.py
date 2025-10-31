
from dataclasses import dataclass, asdict


@dataclass
class StatusBioDTO:
    '''Status biography data transfer object'''
    id: int
    user_id: int
    biography: str

    @classmethod
    def from_model(cls, model: 'StatusBiography') -> 'StatusBioDTO':
        '''Create DTO from database model
        Args:
            model (StatusBiography): database model object
        Returns:
            StatusBioDTO: data transfer object
        '''
        return cls(id=model.id, user_id=model.user_id, biography=model.biography)

    def to_dict(self) -> dict:
        '''Convert to dictionary format
        Returns:
            dict: dictionary format data
        '''
        return asdict(self)
