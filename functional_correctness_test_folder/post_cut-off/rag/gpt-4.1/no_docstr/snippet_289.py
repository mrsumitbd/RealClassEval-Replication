from dataclasses import dataclass, asdict, field
from typing import Any, Dict


@dataclass
class UpdateRuleDeployment:
    '''Model for updating rule deployment.'''

    def __post_init__(self):
        '''Post initilizaiton for validating/converting attributes'''
        # No specific validation/conversion required by default
        pass

    def to_dict(self) -> Dict[str, Any]:
        '''Convert to dictionary for JSON serialization.'''
        return asdict(self)
