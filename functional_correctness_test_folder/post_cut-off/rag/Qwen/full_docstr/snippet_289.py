
from dataclasses import dataclass, field
from typing import Any, Dict


@dataclass
class UpdateRuleDeployment:
    '''Model for updating rule deployment.'''
    rule_id: str
    deployment_id: str
    status: str
    parameters: Dict[str, Any] = field(default_factory=dict)

    def __post_init__(self):
        '''Post initialization for validating/converting attributes'''
        if not isinstance(self.rule_id, str):
            raise ValueError("rule_id must be a string")
        if not isinstance(self.deployment_id, str):
            raise ValueError("deployment_id must be a string")
        if not isinstance(self.status, str):
            raise ValueError("status must be a string")
        if not isinstance(self.parameters, dict):
            raise ValueError("parameters must be a dictionary")

    def to_dict(self) -> Dict[str, Any]:
        '''Convert to dictionary for JSON serialization.'''
        return {
            'rule_id': self.rule_id,
            'deployment_id': self.deployment_id,
            'status': self.status,
            'parameters': self.parameters
        }
