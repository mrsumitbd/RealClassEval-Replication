from dataclasses import dataclass, field, fields as dataclass_fields, is_dataclass
from datetime import datetime
from typing import Any, Dict, List, Optional


@dataclass
class UpdateRuleDeployment:
    '''Model for updating rule deployment.'''
    rule_id: Optional[str] = None
    name: Optional[str] = None
    description: Optional[str] = None
    enabled: Optional[bool] = None
    schedule: Optional[str] = None
    parameters: Optional[Dict[str, Any]] = None
    metadata: Optional[Dict[str, Any]] = None
    tags: Optional[List[str]] = None

    def __post_init__(self):
        '''Post initilizaiton for validating/converting attributes'''
        if isinstance(self.enabled, str):
            v = self.enabled.strip().lower()
            if v in {'true', '1', 'yes', 'y', 'on'}:
                self.enabled = True
            elif v in {'false', '0', 'no', 'n', 'off', ''}:
                self.enabled = False
            else:
                raise ValueError(f"Invalid enabled value: {self.enabled!r}")
        elif isinstance(self.enabled, int):
            self.enabled = bool(self.enabled)
        elif self.enabled is not None and not isinstance(self.enabled, bool):
            raise TypeError("enabled must be a bool")

        if isinstance(self.tags, str):
            self.tags = [t for t in (x.strip()
                                     for x in self.tags.split(',')) if t]
        if self.tags is not None:
            if not isinstance(self.tags, list) or not all(isinstance(t, str) for t in self.tags):
                raise TypeError("tags must be a list of strings")

        if self.parameters is not None and not isinstance(self.parameters, dict):
            raise TypeError("parameters must be a dict")
        if self.metadata is not None and not isinstance(self.metadata, dict):
            raise TypeError("metadata must be a dict")

        if isinstance(self.schedule, datetime):
            self.schedule = self.schedule.isoformat()

        for attr in ('rule_id', 'name', 'description', 'schedule'):
            val = getattr(self, attr)
            if val is not None and not isinstance(val, str):
                raise TypeError(f"{attr} must be a string")

    def to_dict(self) -> Dict[str, Any]:
        '''Convert to dictionary for JSON serialization.'''
        def transform(value: Any) -> Any:
            if value is None:
                return None
            if isinstance(value, datetime):
                return value.isoformat()
            if is_dataclass(value):
                return {
                    f.name: v
                    for f in dataclass_fields(value)
                    for v in [transform(getattr(value, f.name))]
                    if v is not None
                }
            if hasattr(value, "to_dict") and callable(getattr(value, "to_dict")):
                return value.to_dict()
            if isinstance(value, list):
                return [transform(v) for v in value]
            if isinstance(value, tuple):
                return [transform(v) for v in value]
            if isinstance(value, dict):
                return {str(k): transform(v) for k, v in value.items() if v is not None}
            return value

        return {
            f.name: transformed
            for f in dataclass_fields(self)
            for transformed in [transform(getattr(self, f.name))]
            if transformed is not None
        }
