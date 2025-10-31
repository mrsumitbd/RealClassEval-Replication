from dataclasses import dataclass, field
from typing import Any, Dict


@dataclass
class StatusBioDTO:
    '''Status biography data transfer object'''
    data: Dict[str, Any] = field(default_factory=dict)

    @classmethod
    def from_model(cls, model: 'StatusBiography') -> 'StatusBioDTO':
        '''Create DTO from database model
        Args:
            model (StatusBiography): database model object
        Returns:
            StatusBioDTO: data transfer object
        '''
        payload: Dict[str, Any] = {}
        # Prefer __dict__ for performance and to avoid descriptor access where possible
        raw = {}
        try:
            raw = dict(vars(model))
        except Exception:
            # Fallback: inspect attributes via dir
            for name in dir(model):
                if name.startswith('_'):
                    continue
                try:
                    value = getattr(model, name)
                except Exception:
                    continue
                raw[name] = value

        for key, value in raw.items():
            if key.startswith('_'):
                continue
            # Filter out common ORM internal attributes
            if key in {'metadata', 'registry'}:
                continue
            # Skip callables
            if callable(value):
                continue
            payload[key] = value

        return cls(data=payload)

    def to_dict(self) -> dict:
        '''Convert to dictionary format
        Returns:
            dict: dictionary format data
        '''
        return dict(self.data)
