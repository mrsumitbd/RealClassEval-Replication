
from dataclasses import dataclass, asdict
from typing import Dict, Any


@dataclass
class UpdateRuleDeployment:
    '''Model for updating rule deployment.'''

    def __post_init__(self):
        pass

    def to_dict(self) -> Dict[str, Any]:
        '''Convert to dictionary for JSON serialization.'''
        return asdict(self)
