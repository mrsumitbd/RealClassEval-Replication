
from dataclasses import dataclass, field
from typing import Any, Dict


@dataclass
class StatusBioDTO:
    data: Dict[str, Any] = field(default_factory=dict)

    @classmethod
    def from_model(cls, model: 'StatusBiography') -> 'StatusBioDTO':
        """
        Create a DTO instance from a StatusBiography model instance.
        All public attributes of the model that are not callable are copied.
        """
        # Extract attributes that are not private and not callable
        attrs = {
            key: value
            for key, value in vars(model).items()
            if not key.startswith('_') and not callable(value)
        }
        return cls(data=attrs)

    def to_dict(self) -> dict:
        """
        Return the DTO data as a plain dictionary.
        """
        return dict(self.data)
