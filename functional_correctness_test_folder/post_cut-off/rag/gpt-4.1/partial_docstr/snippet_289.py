from dataclasses import dataclass, asdict, field
from typing import Any, Dict


@dataclass
class UpdateRuleDeployment:
    '''Model for updating rule deployment.'''

    # Example fields (since none are specified in the skeleton)
    rule_id: str = field(default="")
    status: str = field(default="")
    updated_by: str = field(default="")
    updated_at: Any = field(default=None)

    def __post_init__(self):
        '''Post initilizaiton for validating/converting attributes'''
        if not isinstance(self.rule_id, str):
            self.rule_id = str(self.rule_id)
        if not isinstance(self.status, str):
            self.status = str(self.status)
        if self.updated_at is not None and not isinstance(self.updated_at, str):
            self.updated_at = str(self.updated_at)

    def to_dict(self) -> Dict[str, Any]:
        '''Convert to dictionary for JSON serialization.'''
        return asdict(self)
