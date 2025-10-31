from dataclasses import dataclass, fields, MISSING, asdict
from typing import Dict, Any, TypeVar, Type

T = TypeVar('T', bound='Program')


@dataclass
class Program:
    '''Represents a program in the database'''

    def to_dict(self) -> Dict[str, Any]:
        '''Convert to dictionary representation'''
        return asdict(self)

    @classmethod
    def from_dict(cls: Type[T], data: Dict[str, Any]) -> T:
        '''Create from dictionary representation'''
        if not isinstance(data, dict):
            raise TypeError("data must be a dict")
        cls_fields = {f.name: f for f in fields(cls)}
        init_kwargs: Dict[str, Any] = {}
        for name, f in cls_fields.items():
            if name in data:
                init_kwargs[name] = data[name]
            else:
                if f.default is not MISSING or f.default_factory is not MISSING:
                    continue
                raise KeyError(f"Missing required field: {name}")
        return cls(**init_kwargs)
