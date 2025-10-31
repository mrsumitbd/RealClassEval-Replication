
from dataclasses import dataclass, field, asdict
from typing import Optional, Dict, Any


@dataclass
class UpdateRuleDeployment:
    '''Model for updating rule deployment.'''
    name: Optional[str] = None
    enabled: Optional[bool] = None
    description: Optional[str] = None
    version: Optional[int] = None

    def __post_init__(self):
        '''Post initilizaiton for validating/converting attributes'''
        if self.name is not None and not isinstance(self.name, str):
            raise TypeError("name must be a string or None")
        if self.enabled is not None and not isinstance(self.enabled, bool):
            raise TypeError("enabled must be a bool or None")
        if self.description is not None and not isinstance(self.description, str):
            raise TypeError("description must be a string or None")
        if self.version is not None:
            if not isinstance(self.version, int):
                raise TypeError("version must be an int or None")
            if self.version < 0:
                raise ValueError("version must be non-negative")

    def to_dict(self) -> Dict[str, Any]:
        '''Convert to dictionary for JSON serialization.'''
        result = {}
        for k, v in asdict(self).items():
            if v is not None:
                result[k] = v
        return result
