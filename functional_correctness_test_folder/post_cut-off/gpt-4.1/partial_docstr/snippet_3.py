
from dataclasses import dataclass


@dataclass
class StatusBioDTO:
    '''Status biography data transfer object'''
    id: int
    user_id: int
    status: str
    bio: str

    @classmethod
    def from_model(cls, model: 'StatusBiography') -> 'StatusBioDTO':
        '''Create DTO from database model
        Args:
            model (StatusBiography): database model object
        Returns:
            StatusBioDTO: data transfer object
        '''
        return cls(
            id=model.id,
            user_id=model.user_id,
            status=model.status,
            bio=model.bio
        )

    def to_dict(self) -> dict:
        return {
            'id': self.id,
            'user_id': self.user_id,
            'status': self.status,
            'bio': self.bio
        }
