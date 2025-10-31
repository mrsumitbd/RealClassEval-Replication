
from dataclasses import dataclass, asdict


@dataclass
class StatusBioDTO:
    status: str
    biography: str

    @classmethod
    def from_model(cls, model: 'StatusBiography') -> 'StatusBioDTO':
        return cls(status=model.status, biography=model.biography)

    def to_dict(self) -> dict:
        return asdict(self)
