
from dataclasses import dataclass, asdict
from typing import Dict, Any


@dataclass
class StatusBioDTO:

    @classmethod
    def from_model(cls, model: 'StatusBiography') -> 'StatusBioDTO':
        return cls(**model.__dict__)

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)
