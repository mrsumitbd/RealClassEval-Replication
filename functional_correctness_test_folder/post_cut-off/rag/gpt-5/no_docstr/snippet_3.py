from dataclasses import dataclass, fields, asdict, is_dataclass
from typing import Type, TypeVar, Dict, Any

T = TypeVar('T', bound='StatusBioDTO')


@dataclass
class StatusBioDTO:
    '''Status biography data transfer object'''
    @classmethod
    def from_model(cls: Type[T], model: 'StatusBiography') -> T:
        '''Create DTO from database model
        Args:
            model (StatusBiography): database model object
        Returns:
            StatusBioDTO: data transfer object
        '''
        data: Dict[str, Any] = {}
        if isinstance(model, dict):
            for f in fields(cls):
                if f.name in model:
                    data[f.name] = model[f.name]
        else:
            for f in fields(cls):
                if hasattr(model, f.name):
                    data[f.name] = getattr(model, f.name)
        return cls(**data)

    def to_dict(self) -> dict:
        '''Convert to dictionary format
        Returns:
            dict: dictionary format data
        '''
        result: Dict[str, Any] = {}
        for f in fields(self):
            value = getattr(self, f.name)
            if value is None:
                continue
            if is_dataclass(value):
                result[f.name] = asdict(value)
            elif hasattr(value, 'to_dict') and callable(getattr(value, 'to_dict')):
                result[f.name] = value.to_dict()
            else:
                result[f.name] = value
        return result
