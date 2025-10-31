from dataclasses import dataclass, is_dataclass, asdict
from typing import Dict, Any


@dataclass
class Program:
    '''Represents a program in the database'''

    def to_dict(self) -> Dict[str, Any]:
        '''Convert to dictionary representation'''
        def _serialize(value: Any) -> Any:
            if is_dataclass(value):
                return asdict(value)
            if hasattr(value, "to_dict") and callable(getattr(value, "to_dict")):
                try:
                    return value.to_dict()
                except Exception:
                    pass
            if isinstance(value, dict):
                return {k: _serialize(v) for k, v in value.items()}
            if isinstance(value, (list, tuple, set)):
                t = type(value)
                return t(_serialize(v) for v in value)
            return value

        return {k: _serialize(v) for k, v in self.__dict__.items()}

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Program':
        '''Create from dictionary representation'''
        if data is None:
            return None
        if not isinstance(data, dict):
            raise TypeError("data must be a dictionary")
        obj = cls()
        for key, value in data.items():
            setattr(obj, key, value)
        return obj
