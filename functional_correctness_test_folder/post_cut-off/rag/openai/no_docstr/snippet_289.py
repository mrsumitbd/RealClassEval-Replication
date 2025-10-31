
from dataclasses import dataclass
from typing import Any, Dict


@dataclass
class UpdateRuleDeployment:
    '''Model for updating rule deployment.'''

    def __post_init__(self):
        '''Post initilizaiton for validating/converting attributes'''
        # No specific validation logic required for the generic model
        pass

    def to_dict(self) -> Dict[str, Any]:
        '''Convert to dictionary for JSON serialization.'''
        # Return a shallow copy of the instance's __dict__ excluding private attributes
        return {k: v for k, v in self.__dict__.items() if not k.startswith('_')}
