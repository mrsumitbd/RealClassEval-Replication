
from dataclasses import dataclass, asdict
from typing import Dict, Any


@dataclass
class UpdateRuleDeployment:
    '''Model for updating rule deployment.'''

    # Assuming some attributes for the dataclass
    id: int
    name: str
    description: str
    is_enabled: bool

    def __post_init__(self):
        '''Post initialization for validating/converting attributes'''
        if not isinstance(self.id, int) or self.id <= 0:
            raise ValueError("ID must be a positive integer")
        if not isinstance(self.name, str) or not self.name.strip():
            raise ValueError("Name must be a non-empty string")
        if not isinstance(self.description, str):
            raise ValueError("Description must be a string")
        if not isinstance(self.is_enabled, bool):
            raise ValueError("Is enabled must be a boolean")

    def to_dict(self) -> Dict[str, Any]:
        '''Convert to dictionary for JSON serialization.'''
        return asdict(self)
