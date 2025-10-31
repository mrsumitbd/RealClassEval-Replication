from dataclasses import dataclass, asdict, fields
from typing import Any, Dict


@dataclass
class Program:
    '''Represents a program in the database'''

    def to_dict(self) -> Dict[str, Any]:
        '''Convert to dictionary representation'''
        def prune_none(obj: Any) -> Any:
            if isinstance(obj, dict):
                return {k: prune_none(v) for k, v in obj.items() if v is not None}
            if isinstance(obj, list):
                return [prune_none(v) for v in obj if v is not None]
            if isinstance(obj, tuple):
                return tuple(prune_none(v) for v in obj if v is not None)
            return obj

        return prune_none(asdict(self))

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Program':
        '''Create from dictionary representation'''
        if data is None:
            return None  # type: ignore[return-value]
        if not isinstance(data, dict):
            raise TypeError('data must be a dict')
        field_names = {f.name for f in fields(cls)}
        init_kwargs = {k: v for k, v in data.items() if k in field_names}
        return cls(**init_kwargs)
