
from dataclasses import dataclass, field
from typing import Any, Dict


@dataclass
class UpdateRuleDeployment:
    '''Model for updating rule deployment.'''
    rule_id: str
    new_version: str
    deployment_time: str
    environment: str = field(default='production')

    def __post_init__(self):
        '''Post initialization for validating/converting attributes'''
        if not isinstance(self.rule_id, str):
            raise ValueError("rule_id must be a string")
        if not isinstance(self.new_version, str):
            raise ValueError("new_version must be a string")
        if not isinstance(self.deployment_time, str):
            raise ValueError("deployment_time must be a string")
        if not isinstance(self.environment, str):
            raise ValueError("environment must be a string")

    def to_dict(self) -> Dict[str, Any]:
        '''Convert to dictionary for JSON serialization.'''
        return {
            'rule_id': self.rule_id,
            'new_version': self.new_version,
            'deployment_time': self.deployment_time,
            'environment': self.environment
        }
