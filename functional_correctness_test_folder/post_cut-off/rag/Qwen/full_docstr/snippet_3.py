
from dataclasses import dataclass, asdict
from typing import Optional


@dataclass
class StatusBioDTO:
    '''Status biography data transfer object'''
    bio: Optional[str] = None
    user_id: Optional[int] = None
    last_updated: Optional[str] = None

    @classmethod
    def from_model(cls, model: 'StatusBiography') -> 'StatusBioDTO':
        '''Create DTO from database model
        Args:
            model (StatusBiography): database model object
        Returns:
            StatusBioDTO: data transfer object
        '''
        return cls(
            bio=model.bio,
            user_id=model.user_id,
            last_updated=model.last_updated
        )

    def to_dict(self) -> dict:
        '''Convert to dictionary format
        Returns:
            dict: dictionary format data
        '''
        return asdict(self)
