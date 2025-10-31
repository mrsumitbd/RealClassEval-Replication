from dataclasses import dataclass, fields, is_dataclass
from datetime import datetime, date
from typing import Any, Dict
import enum


def _to_serializable(value: Any) -> Any:
    if value is None:
        return None
    if isinstance(value, (datetime, date)):
        return value.isoformat()
    if isinstance(value, enum.Enum):
        return value.value
    if isinstance(value, set):
        return [_to_serializable(v) for v in value]
    if isinstance(value, (list, tuple)):
        return [_to_serializable(v) for v in value]
    if isinstance(value, dict):
        return {k: _to_serializable(v) for k, v in value.items() if v is not None}
    if is_dataclass(value):
        # Recursively convert nested dataclasses
        return {f.name: _to_serializable(getattr(value, f.name)) for f in fields(value) if getattr(value, f.name) is not None}
    return value


@dataclass
class UpdateRuleDeployment:
    '''Model for updating rule deployment.'''

    def __post_init__(self):
        '''Post initilizaiton for validating/converting attributes'''
        for f in fields(self):
            v = getattr(self, f.name)
            if isinstance(v, enum.Enum):
                setattr(self, f.name, v.value)
            elif isinstance(v, (datetime, date)):
                setattr(self, f.name, v.isoformat())
            elif isinstance(v, set):
                setattr(self, f.name, list(v))
            elif isinstance(v, tuple):
                setattr(self, f.name, list(v))

    def to_dict(self) -> Dict[str, Any]:
        '''Convert to dictionary for JSON serialization.'''
        result: Dict[str, Any] = {}
        for f in fields(self):
            value = getattr(self, f.name)
            if value is None:
                continue
            result[f.name] = _to_serializable(value)
        return result
