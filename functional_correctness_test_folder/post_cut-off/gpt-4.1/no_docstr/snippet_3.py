
from dataclasses import dataclass


@dataclass
class StatusBioDTO:
    id: int
    status: str
    biography: str

    @classmethod
    def from_model(cls, model: 'StatusBiography') -> 'StatusBioDTO':
        return cls(
            id=model.id,
            status=model.status,
            biography=model.biography
        )

    def to_dict(self) -> dict:
        return {
            'id': self.id,
            'status': self.status,
            'biography': self.biography
        }
