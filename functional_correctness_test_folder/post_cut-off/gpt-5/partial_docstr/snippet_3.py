from dataclasses import dataclass
from typing import Any, Dict


@dataclass
class StatusBioDTO:
    '''Status biography data transfer object'''
    data: Dict[str, Any]

    @classmethod
    def from_model(cls, model: 'StatusBiography') -> 'StatusBioDTO':
        '''Create DTO from database model
        Args:
            model (StatusBiography): database model object
        Returns:
            StatusBioDTO: data transfer object
        '''
        if model is None:
            raise ValueError("model must not be None")

        # Prefer explicit to_dict method if available
        if hasattr(model, "to_dict") and callable(getattr(model, "to_dict")):
            data = dict(model.to_dict())
            return cls(data=data)

        # If already a mapping
        if isinstance(model, dict):
            return cls(data=dict(model))

        # Try __dict__ for typical ORM/objects
        if hasattr(model, "__dict__"):
            items = {
                k: v
                for k, v in vars(model).items()
                if not k.startswith("_") and not callable(v)
            }
            return cls(data=items)

        # Fallback: inspect attributes via dir()
        collected: Dict[str, Any] = {}
        for name in dir(model):
            if name.startswith("_"):
                continue
            try:
                value = getattr(model, name)
            except Exception:
                continue
            if callable(value):
                continue
            collected[name] = value

        return cls(data=collected)

    def to_dict(self) -> dict:
        return dict(self.data)
