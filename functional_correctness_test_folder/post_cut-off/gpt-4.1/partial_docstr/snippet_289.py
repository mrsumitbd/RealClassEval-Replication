
from dataclasses import dataclass, field, asdict
from typing import Any, Dict, Optional


@dataclass
class UpdateRuleDeployment:
    '''Model for updating rule deployment.'''
    name: Optional[str] = None
    enabled: Optional[bool] = None
    description: Optional[str] = None
    version: Optional[str] = None
    parameters: Optional[Dict[str, Any]] = field(default_factory=dict)

    def __post_init__(self):
        if self.parameters is None:
            self.parameters = {}

    def to_dict(self) -> Dict[str, Any]:
        result = asdict(self)
        # Remove keys with value None
        return {k: v for k, v in result.items() if v is not None}
